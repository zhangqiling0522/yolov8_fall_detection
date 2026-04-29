# 基于YOLOv8的摔倒智能检测系统


## 项目简介

本项目是一个基于YOLOv8的摔倒智能检测系统，旨在为养老院、医院等场所提供实时的老人安全监测服务。系统通过摄像头或视频文件进行实时摔倒检测，结合姿态估计技术区分躺卧、弯腰、站立等姿势，并通过时序间隔机制降低误报率。当检测到摔倒时，系统会通过前端界面和硬件蜂鸣器发出警报。

## 项目结构

```
yolov8_fall_detection/
├── backend/                    # 后端代码
│   ├── main.py                 # FastAPI应用主文件
│   ├── database.py             # 数据库连接配置
│   ├── models.py               # 数据库模型定义
│   ├── init_db.py              # 数据库初始化脚本
│   ├── requirements.txt        # 后端依赖列表
│   └── ...                     # 其他辅助脚本
├── src/                        # 前端代码
│   ├── components/             # 组件目录
│   │   └── Login.vue           # 登录组件
│   ├── views/                  # 页面目录
│   │   ├── Home.vue            # 实时监测页面
│   │   └── Profile.vue         # 个人中心页面
│   ├── router/                 # 路由配置
│   │   └── index.js            # 路由定义
│   ├── pic/                    # 图片资源
│   ├── App.vue                 # 根组件
│   ├── main.js                 # 入口文件
│   └── style.css               # 全局样式
├── dataSet/                    # 数据集
│   ├── train/                  # 训练集
│   ├── valid/                  # 验证集
│   └── fall.yaml               # 数据集配置文件
├── buzzer.ino/                 # Arduino代码
├── runs/                       # 模型训练结果（运行后生成）
├── api_test.py                 # API性能测试脚本
├── train.py                    # 模型训练脚本
├── detect_fall.py              # 批量检测脚本
├── package.json                # 前端依赖配置
└── vite.config.js              # Vite配置
```

## 功能特性

- **实时摔倒检测**：基于YOLOv8目标检测模型，实时分析视频流
- **姿态估计**：集成YOLOv8姿态估计模型，分析人体关键点
- **智能报警**：连续检测摔倒触发报警
- **多源视频输入**：支持摄像头实时流和本地视频文件
- **硬件集成**：支持通过Arduino控制蜂鸣器实现物理报警
- **数据管理**：基于SQLite数据库管理老人信息、管理员信息和检测日志
- **用户友好界面**：使用Vue 3构建直观的前端界面

## 技术栈

### 前端
- **框架**：Vue 3
- **构建工具**：Vite
- **路由**：Vue Router
- **HTTP客户端**：Axios

### 后端
- **框架**：FastAPI
- **数据库**：SQLite + SQLAlchemy
- **目标检测**：YOLOv8
- **姿态估计**：YOLOv8 Pose
- **串口通信**：pyserial

### 硬件
- **开发板**：Arduino Uno
- **传感器**：蜂鸣器、按钮

## 环境要求

### 硬件要求
- **CPU**：Intel Core i5及以上
- **内存**：8GB及以上
- **存储**：至少50GB可用空间
- **摄像头**：USB摄像头或网络摄像头（可选）
- **GPU**：NVIDIA GPU（推荐，用于加速模型推理）

### 软件要求
- **操作系统**：Windows 10/11 或 Ubuntu 20.04+
- **Python**：3.8+
- **Node.js**：16+




## 模型训练

### 数据集准备

确保数据集按照YOLO格式组织：

```
dataSet/
├── train/
│   ├── images/                 # 训练图像
│   └── labels/                 # 训练标注
├── valid/
│   ├── images/                 # 验证图像
│   └── labels/                 # 验证标注
└── fall.yaml                   # 数据集配置
```

### 运行训练

```bash
python train.py
```

训练完成后，模型权重保存在 `runs/detect/train*/weights/best.pt`

### 模型评估

训练过程中会自动评估模型性能，包括精确率、召回率和mAP指标。

## API接口

### 认证接口

**POST /login** - 管理员登录

请求体：
```json
{
    "name": "小张",
    "phone": "13800138004",
    "password": "123456"
}
```

响应：
```json
{
    "success": true,
    "message": "登录成功",
    "admin_id": "0001",
    "admin_name": "小张"
}
```

### 检测接口

**POST /detect/fall** - 摔倒检测

请求：`multipart/form-data` 包含图像文件

响应：
```json
{
    "success": true,
    "fall_detected": true,
    "fall_count": 1,
    "poses": [...],
    "image": "data:image/jpeg;base64,..."
}
```

### 数据管理接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /old-persons | 获取老人列表 |
| GET | /old-persons/room/{room_number} | 根据房间号获取老人信息 |
| GET | /admins | 获取管理员列表 |
| POST | /admins | 添加管理员 |
| GET | /logs | 获取日志列表 |
| POST | /logs/fall-detection | 记录摔倒事件 |
| DELETE | /logs/{log_id} | 删除日志 |

### 硬件控制接口

**POST /alarm/stop** - 停止报警

响应：
```json
{
    "success": true,
    "message": "报警已停止"
}
```

## 前端使用

### 登录页面

- 输入管理员姓名、手机号和密码
- 点击登录按钮进入系统

### 实时监测页面

- **视频区域**：显示摄像头实时流或视频文件
- **检测状态**：显示当前检测状态、预警房间号、检测人数、摔倒人数
- **警报灯**：蓝色（未检测）、绿色（正常）、红色闪烁（报警）
- **停止报警按钮**：点击停止报警
- **记录查询**：支持按时间、房间号和姓名查询日志

### 个人中心页面

- **个人信息**：显示当前登录管理员的基本信息
- **员工管理**：查看和添加管理员

## 硬件集成

### Arduino连接

1. 将Arduino通过USB连接到电脑
2. 上传Arduino代码到开发板
3. 启动后端服务，系统会自动检测Arduino设备

### Arduino代码

```cpp
const int buzzerPin = 8;
const int buttonPin = 7;
const int lightPin = 12;
bool alarm = false;
unsigned long previousMillis = 0;  // 记录上一次LED闪烁时间
const long blinkInterval = 500;
void setup() {
  pinMode(buzzerPin, OUTPUT);
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(lightPin, OUTPUT);
  Serial.begin(9600);
  digitalWrite(buzzerPin, LOW);
  digitalWrite(lightPin, LOW);
}
void loop() {
  if (Serial.available()) {
    char cmd = Serial.read();
    if (cmd == 'S' || cmd == 's') {
      alarm = true;
    }
    if (cmd == 'X' || cmd == 'x') {
      alarm = false;
    }
  }
  if (digitalRead(buttonPin) == LOW) {
    alarm = false;
  }
  digitalWrite(buzzerPin, alarm ? HIGH : LOW);
  if (alarm) {
    unsigned long currentMillis = millis();
    if (currentMillis - previousMillis >= blinkInterval) {
      previousMillis = currentMillis;  // 更新时间
      digitalWrite(lightPin, !digitalRead(lightPin));  // 翻转LED状态
    }
  } else {
    digitalWrite(lightPin, LOW);
  }
}
```

## 部署说明

### 开发环境

直接运行前端和后端开发服务器即可：

```bash
# 后端
cd backend
python main.py

# 前端
npm run dev
```

### 生产环境

1. **构建前端**：
   ```bash
   npm run build
   ```

2. **配置Nginx**：
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           root /path/to/dist;
           index index.html;
           try_files $uri $uri/ /index.html;
       }
       
       location /api {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
       }
   }
   ```

3. **启动后端服务**：
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## 测试

### API性能测试

运行API测试脚本：

```bash
python api_test.py
```

测试完成后会生成：
- `api_test_results.json` - 测试结果数据
- `api_response_times.png` - 响应时间趋势图
- `api_response_boxplot.png` - 响应时间分布图
- `api_response_bar.png` - 响应时间对比图
- `api_combined_chart.png` - 组合图表

## 本地验证快速开始

### 1. 克隆项目

```bash
git clone https://github.com/zhangqiling0522/yolov8_fall_detection.git
cd yolov8_fall_detection
```

### 2. 安装后端依赖

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 3. 安装前端依赖

```bash
cd ..
npm install
```

### 4. 初始化数据库

```bash
cd backend
python init_db.py
```

### 5. 启动后端服务

```bash
python main.py
```

### 6. 启动前端开发服务器

```bash
cd ..
npm run dev
```

