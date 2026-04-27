from ultralytics import YOLO
import cv2
import os

# 加载训练好的模型
model = YOLO('runs/detect/train/weights/best.pt')  # 加载训练好的最佳模型

# 测试图片目录
test_dir = 'dataSet/test/images'

# 遍历测试图片
for img_name in os.listdir(test_dir):
    if img_name.endswith('.jpg'):
        img_path = os.path.join(test_dir, img_name)
        
        # 执行预测
        results = model(img_path)
        
        # 显示结果
        result = results[0]
        img = cv2.imread(img_path)
        
        # 绘制边界框
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = box.conf[0].item()
            cls = box.cls[0].item()
            
            # 绘制矩形
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            
            # 添加标签
            label = f'fall: {conf:.2f}'
            cv2.putText(img, label, (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        # 显示结果
        cv2.imshow('Result', img)
        cv2.waitKey(0)

cv2.destroyAllWindows()
