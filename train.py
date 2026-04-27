from ultralytics import YOLO

if __name__ == '__main__':
    # 加载预训练模型
    model = YOLO('yolov8n.pt')  # 使用n版本的YOLOv8，适合小显存设备

    # 训练模型
    results = model.train(
        data='dataSet/fall.yaml',  # 数据集配置文件路径
        epochs=100,  # 训练轮数
        batch=8,  # 批次大小
        imgsz=640,  # 输入图像大小
        device=0,  # 使用显卡（GPU 0）
        workers=0,  # Windows系统设置为0以避免多进程问题
        verbose=True  # 显示详细训练过程
    )
