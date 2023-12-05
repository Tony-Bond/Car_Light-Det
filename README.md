# Car Light Det
**Car light detect based on yolov8！**

## 效果展示
![](docs/1.jpg)

## 1. Train bdd100k
### 1.1 bdd100k dataset structure
```txt
bdd100k
└── images
    ├── images
    │   ├── train
    │   │   └── 0a0a0b1a-7c39d841.jpg
    │   └── val
    │       └── b1c9c847-3bda4659.jpg
    └── labels
        ├── bdd100k_labels_images_train.json
        └── bdd100k_labels_images_val.json
```
### 1.2 train
```bash
python train_bdd.py
```

## 2. 车灯训练
略

## 3. 推理
```bash
python inference.py
```

