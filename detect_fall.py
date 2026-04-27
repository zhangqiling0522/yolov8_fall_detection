import os
import cv2
import numpy as np
from ultralytics import YOLO

# 加载训练好的模型
model_path = 'runs/detect/train8/weights/best.pt'
model = YOLO(model_path)

# 图片路径和结果保存路径
input_dir = 'archive/detect'
output_dir = 'detect_result'

# 创建输出目录
os.makedirs(output_dir, exist_ok=True)

# 获取所有图片文件
image_files = [f for f in os.listdir(input_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
print(f'找到 {len(image_files)} 张图片')

# 存储处理后的图片
processed_images = []

# 处理每张图片
for i, image_file in enumerate(image_files):
    print(f'处理第 {i+1} 张图片: {image_file}')
    
    # 读取图片
    image_path = os.path.join(input_dir, image_file)
    image = cv2.imread(image_path)
    
    if image is None:
        print(f'无法读取图片: {image_file}')
        continue
    
    # 检测摔倒
    results = model(image)
    
    # 标注结果
    annotated_image = image.copy()
    
    # 遍历检测结果
    for result in results:
        boxes = result.boxes
        for box in boxes:
            # 获取边界框坐标
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            # 获取置信度
            conf = box.conf[0]
            # 获取类别
            cls = int(box.cls[0])
            
            # 如果是摔倒类别（假设0是摔倒）
            if cls == 0 and conf > 0.5:
                # 绘制红框
                cv2.rectangle(annotated_image, (x1, y1), (x2, y2), (0, 0, 255), 2)
                # 添加标签
                label = f'fall: {conf:.2f}'
                cv2.putText(annotated_image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
    # 保存标注后的图片
    output_path = os.path.join(output_dir, image_file)
    cv2.imwrite(output_path, annotated_image)
    
    # 调整图片尺寸为统一大小
    target_size = (200, 200)  # 设置目标尺寸
    resized_image = cv2.resize(annotated_image, target_size)
    
    # 添加到处理列表
    processed_images.append(resized_image)
    
    # 每9张图片拼成一张大图
    if (i + 1) % 9 == 0 or (i + 1) == len(image_files):
        if len(processed_images) > 0:
            # 创建拼图
            grid_size = 3  # 3x3网格
            target_size = (200, 200)  # 统一尺寸
            
            # 创建空白大图
            grid_img = np.zeros((grid_size * target_size[0], grid_size * target_size[1], 3), dtype=np.uint8)
            
            # 填充图片
            for j, img in enumerate(processed_images):
                row = j // grid_size
                col = j % grid_size
                if row < grid_size and col < grid_size:
                    grid_img[row * target_size[0]:(row + 1) * target_size[0], col * target_size[1]:(col + 1) * target_size[1]] = img
            
            # 保存拼图
            grid_output_path = os.path.join(output_dir, f'grid_{i//9 + 1}.jpg')
            cv2.imwrite(grid_output_path, grid_img)
            print(f'保存拼图: {grid_output_path}')
            
            # 清空处理列表
            processed_images = []

print('检测完成！')