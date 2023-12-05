"""训练脚本
"""
from ultralytics import YOLO

# model = YOLO('yolov8x.yaml')  # 从YAML构建新模型

# 加载模型
model = YOLO('yolov8x.pt')  # 加载预训练模型（推荐用于训练）

# 使用4个GPU训练模型
results = model.train(
    data='/root/ultralytics/bdd100k.yaml', 
    batch=64, 
    epochs=300, 
    imgsz=640, 
    cache=True, 
    device=[1, 2, 3, 4], 
    lr0=0.001, 
    cos_lr=True, 
    workers=16
)

# Evaluate the model's performance on the validation set
results = model.val()
