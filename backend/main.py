from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db
from models import OldPerson, Admin, Log, TestData, SceneEnum, DetectionResultEnum
import datetime
from pydantic import BaseModel
import numpy as np
import cv2
from ultralytics import YOLO
import base64
import io
import serial
import serial.tools.list_ports
from typing import Optional

# 串口通信设置
ser = None

def init_serial():
    global ser
    # 自动检测Arduino串口
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if 'Arduino' in port.description or 'CH340' in port.description:
            try:
                ser = serial.Serial(port.device, 9600, timeout=1)
                print(f"连接到Arduino: {port.device}")
                return True
            except Exception as e:
                print(f"连接Arduino失败: {e}")
    print("未找到Arduino设备")
    return False

# 初始化串口
init_serial()

# 登录请求模型
class LoginRequest(BaseModel):
    name: str
    phone: str
    password: str

# 登录响应模型
class LoginResponse(BaseModel):
    success: bool
    message: str
    admin_id: str = None
    admin_name: str = None

# 添加管理员请求模型
class AdminCreateRequest(BaseModel):
    id: str
    name: str
    age: int
    gender: str
    position: str
    phone: str
    password: str

# 记录摔倒事件请求模型
class FallLogRequest(BaseModel):
    room_number: str
    phone: str
    scene: str = "房间"
    confidence: Optional[float] = None
    detection_result: Optional[str] = None
    admin_id: Optional[str] = None

# 测试数据请求模型
class TestDataRequest(BaseModel):
    test_name: str
    test_type: str
    scene: str
    total_samples: int
    true_positive: int
    false_positive: int
    false_negative: int
    true_negative: int

# 加载训练好的模型
model_path = "../runs/detect/train8/weights/best.pt"
model = YOLO(model_path)

# 加载姿态估计模型
pose_model = YOLO('yolov8n-pose.pt')

# 创建FastAPI应用实例
app = FastAPI(
    title="摔倒智能检测系统API",
    description="基于YOLOv8的摔倒智能检测系统后端API",
    version="1.0.0"
)

# 配置CORS，允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应设置具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 根路径
@app.get("/")
def read_root():
    return {"message": "欢迎使用摔倒智能检测系统API"}

# 健康检查
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# 获取老人列表
@app.get("/old-persons")
def get_old_persons(db: Session = Depends(get_db)):
    old_persons = db.query(OldPerson).all()
    return old_persons

# 获取指定房间的老人信息
@app.get("/old-persons/room/{room_number}")
def get_old_person_by_room(room_number: str, db: Session = Depends(get_db)):
    old_person = db.query(OldPerson).filter(OldPerson.room_number == room_number).first()
    if not old_person:
        raise HTTPException(status_code=404, detail="该房间未找到老人信息")
    return old_person

# 获取管理员列表
@app.get("/admins")
def get_admins(db: Session = Depends(get_db)):
    admins = db.query(Admin).all()
    return admins

# 获取日志列表
@app.get("/logs")
def get_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logs = db.query(Log).offset(skip).limit(limit).all()
    return logs

# 记录摔倒事件
@app.post("/logs/fall-detection")
def create_fall_log(request: FallLogRequest, db: Session = Depends(get_db)):
    # 检查房间是否存在老人
    old_person = db.query(OldPerson).filter(OldPerson.room_number == request.room_number).first()
    if old_person:
        # 使用老人的电话号码
        request.phone = old_person.phone
    
    # 创建日志记录
    new_log = Log(
        room_number=request.room_number,
        phone=request.phone,
        status="摔倒检测",
        scene=request.scene,
        confidence=request.confidence,
        detection_result=request.detection_result,
        admin_id=request.admin_id
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

# 获取场景列表
@app.get("/scenes")
def get_scenes():
    return {
        "scenes": [
            {"value": "房间", "label": "房间"},
            {"value": "大厅", "label": "大厅"},
            {"value": "院落", "label": "院落"}
        ]
    }

# 添加测试数据
@app.post("/test-data")
def create_test_data(data: TestDataRequest, db: Session = Depends(get_db)):
    new_test_data = TestData(
        test_name=data.test_name,
        test_type=data.test_type,
        scene=data.scene,
        total_samples=data.total_samples,
        true_positive=data.true_positive,
        false_positive=data.false_positive,
        false_negative=data.false_negative,
        true_negative=data.true_negative
    )
    db.add(new_test_data)
    db.commit()
    db.refresh(new_test_data)
    return new_test_data

# 获取测试数据列表
@app.get("/test-data")
def get_test_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    test_data = db.query(TestData).offset(skip).limit(limit).all()
    return test_data

# 获取识别率统计
@app.get("/statistics/accuracy")
def get_accuracy_statistics(scene: Optional[str] = None, test_type: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(TestData)
    
    if scene:
        query = query.filter(TestData.scene == scene)
    if test_type:
        query = query.filter(TestData.test_type == test_type)
    
    test_data_list = query.all()
    
    if not test_data_list:
        return {
            "total_samples": 0,
            "precision": 0.0,
            "recall": 0.0,
            "f1_score": 0.0,
            "accuracy": 0.0
        }
    
    # 汇总数据
    total = 0
    tp = 0
    fp = 0
    fn = 0
    tn = 0
    
    for data in test_data_list:
        total += data.total_samples
        tp += data.true_positive
        fp += data.false_positive
        fn += data.false_negative
        tn += data.true_negative
    
    # 计算指标
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    accuracy = (tp + tn) / total if total > 0 else 0.0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return {
        "total_samples": total,
        "true_positive": tp,
        "false_positive": fp,
        "false_negative": fn,
        "true_negative": tn,
        "precision": precision,
        "recall": recall,
        "accuracy": accuracy,
        "f1_score": f1_score
    }

# 获取按场景分组的统计数据
@app.get("/statistics/by-scene")
def get_statistics_by_scene(db: Session = Depends(get_db)):
    scenes = ["房间", "大厅", "院落"]
    results = []
    
    for scene in scenes:
        query = db.query(TestData).filter(TestData.scene == scene)
        test_data_list = query.all()
        
        if test_data_list:
            total = 0
            tp = 0
            fp = 0
            fn = 0
            tn = 0
            
            for data in test_data_list:
                total += data.total_samples
                tp += data.true_positive
                fp += data.false_positive
                fn += data.false_negative
                tn += data.true_negative
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            accuracy = (tp + tn) / total if total > 0 else 0.0
            f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
            
            results.append({
                "scene": scene,
                "total_samples": total,
                "precision": precision,
                "recall": recall,
                "accuracy": accuracy,
                "f1_score": f1_score
            })
    
    return results

# 与同类研究对比
@app.get("/statistics/comparison")
def get_comparison_statistics():
    # 模拟与同类研究的对比数据
    return {
        "comparison": [
            {
                "method": "本系统",
                "precision": 0.925,
                "recall": 0.908,
                "accuracy": 0.931,
                "f1_score": 0.916
            },
            {
                "method": "传统YOLOv5",
                "precision": 0.873,
                "recall": 0.856,
                "accuracy": 0.895,
                "f1_score": 0.864
            },
            {
                "method": "基于骨骼姿态",
                "precision": 0.852,
                "recall": 0.821,
                "accuracy": 0.873,
                "f1_score": 0.836
            },
            {
                "method": "深度传感器",
                "precision": 0.889,
                "recall": 0.867,
                "accuracy": 0.902,
                "f1_score": 0.878
            }
        ]
    }

# 删除指定日志
@app.delete("/logs/{log_id}")
def delete_log(log_id: int, db: Session = Depends(get_db)):
    log = db.query(Log).filter(Log.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="日志不存在")
    db.delete(log)
    db.commit()
    return {"message": "日志删除成功"}

# 管理员登录
@app.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    # 根据姓名、手机号和密码查询管理员
    admin = db.query(Admin).filter(
        Admin.name == login_data.name,
        Admin.phone == login_data.phone,
        Admin.password == login_data.password
    ).first()
    
    if admin:
        return LoginResponse(
            success=True,
            message="登录成功",
            admin_id=admin.id,
            admin_name=admin.name
        )
    else:
        return LoginResponse(
            success=False,
            message="登录失败，请检查姓名、手机号和密码"
        )

# 添加管理员
@app.post("/admins")
def create_admin(admin_data: AdminCreateRequest, db: Session = Depends(get_db)):
    # 检查ID是否已存在
    existing_admin = db.query(Admin).filter(Admin.id == admin_data.id).first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="该管理员ID已存在")
    
    # 创建新管理员
    new_admin = Admin(
        id=admin_data.id,
        name=admin_data.name,
        age=admin_data.age,
        gender=admin_data.gender,
        position=admin_data.position,
        phone=admin_data.phone,
        password=admin_data.password
    )
    
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    
    return {
        "success": True,
        "message": "管理员添加成功",
        "admin": new_admin
    }

# 检测摔倒API
@app.post("/detect/fall")
async def detect_fall(file: UploadFile = File(...)):
    try:
        # 读取图像文件
        contents = await file.read()
        img = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)
        
        if img is None:
            raise HTTPException(status_code=400, detail="无法读取图像")
        
        # 检测摔倒
        results = model(img)
        
        # 标注结果
        annotated_img = img.copy()
        fall_detected = False
        fall_count = 0
        poses = []
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0]
                cls = int(box.cls[0])
                
                # 如果是摔倒类别（假设0是摔倒）且置信度大于0.5
                if cls == 0 and conf > 0.5:
                    # 进行姿态估计
                    pose_results = pose_model(img[y1:y2, x1:x2])
                    
                    # 分析姿态
                    pose = "未知"
                    for pose_result in pose_results:
                        if pose_result.keypoints:
                            # 提取关键点
                            keypoints = pose_result.keypoints.data[0].cpu().numpy()
                            
                            # 分析姿态
                            if len(keypoints) >= 17:
                                # 获取关键关节点
                                nose = keypoints[0][:2]
                                left_shoulder = keypoints[5][:2]
                                right_shoulder = keypoints[6][:2]
                                left_hip = keypoints[11][:2]
                                right_hip = keypoints[12][:2]
                                
                                # 计算身体角度
                                shoulder_y = (left_shoulder[1] + right_shoulder[1]) / 2
                                hip_y = (left_hip[1] + right_hip[1]) / 2
                                
                                # 计算躯干与地面的角度
                                if abs(shoulder_y - hip_y) < 50:
                                    # 躺卧姿势
                                    pose = "躺卧"
                                    fall_detected = True
                                    fall_count += 1
                                elif shoulder_y < hip_y - 100:
                                    # 弯腰姿势
                                    pose = "弯腰"
                                else:
                                    # 站立姿势
                                    pose = "站立"
                    
                    # 绘制红框
                    cv2.rectangle(annotated_img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    # 添加标签
                    label = f'{pose}: {conf:.2f}'
                    cv2.putText(annotated_img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    
                    # 保存姿态信息
                    poses.append({
                        "pose": pose,
                        "confidence": float(conf),
                        "bbox": [int(x1), int(y1), int(x2), int(y2)]
                    })
        
        # 将标注后的图像转换为base64
        retval, buffer = cv2.imencode('.jpg', annotated_img)
        if not retval:
            raise HTTPException(status_code=500, detail="无法编码图像")
        
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        img_data_url = f"data:image/jpeg;base64,{img_base64}"
        
        # 如果检测到摔倒，发送信号给Arduino
        if fall_detected:
            try:
                if ser and ser.is_open:
                    ser.write(b'S')
                    print("发送报警信号到Arduino")
            except Exception as e:
                print(f"发送信号失败: {e}")
        
        # 返回检测结果
        return {
            "success": True,
            "fall_detected": fall_detected,
            "fall_count": fall_count,
            "poses": poses,
            "image": img_data_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"检测失败: {str(e)}")

# 停止报警API
@app.post("/alarm/stop")
def stop_alarm():
    try:
        # 发送停止报警信号给Arduino
        if ser and ser.is_open:
            ser.write(b'X')
            print("发送停止报警信号到Arduino")
            return {"success": True, "message": "报警已停止"}
        else:
            return {"success": False, "message": "未连接到Arduino"}
    except Exception as e:
        print(f"发送停止信号失败: {e}")
        return {"success": False, "message": f"停止报警失败: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    print("后端服务启动中...")
    print("访问地址:")
    print("  本地访问: http://localhost:8000")
    print("  API文档: http://localhost:8000/docs")
    print("  ReDoc文档: http://localhost:8000/redoc")
    print("服务启动后按 CTRL+C 停止")
    print("\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)