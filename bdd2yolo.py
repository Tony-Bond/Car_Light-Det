"""bdd2yolo
"""
import os
import json
from tqdm import tqdm
import cv2

TRAIN_LABEL_NAME = 'bdd100k_labels_images_train.json'
VAL_LABEL_NAME = 'bdd100k_labels_images_val.json'

classes = [
    "person",
    "bike",
    "car",
    "motor",
    "bus",
    "truck",
    "rider",
    "train"
]

counter = {}

for c in classes:
    counter[c] = 0


def get_args():
    """传递参数
    """
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--images', help="images path",
                        type=str, default='/root/ultralytics/bdd100k/images/images')
    parser.add_argument('-l', '--labels', help="labels path",
                        type=str, default="/root/ultralytics/bdd100k/images/labels")
    parser.add_argument('-t', '--type', help="type of dataset",
                        choices=['train', 'val'], default='val')

    return parser.parse_args()


def convertBdd100k2yolo(imageFileName, label):
    """类别映射
    box格式转换
    """
    img = cv2.imread(imageFileName)
    width, height = img.shape[1], img.shape[0]
    dw = 1.0 / width
    dh = 1.0 / height

    catName = label['category']
    classIndex = classes.index(catName)
    roi = label['box2d']

    w = roi['x2'] - roi['x1']
    h = roi['y2'] - roi['y1']
    x_center = roi['x1'] + w / 2
    y_center = roi['y1'] + h / 2

    x_center, y_center, w, h = x_center * dw, y_center * dh, w * dw, h * dh

    return "{} {} {} {} {}\n".format(classIndex, x_center, y_center, w, h)


if __name__ == '__main__':
    args = get_args()
    # 转为文件位置
    if args.type == 'train':
        imageRootPath = os.path.join(args.images, 'train')
        labelFilePath = os.path.join(args.labels, TRAIN_LABEL_NAME)
    else:
        imageRootPath = os.path.join(args.images, 'val')
        labelFilePath = os.path.join(args.labels, VAL_LABEL_NAME)

    with open(labelFilePath) as file:
        lines = json.load(file)
        print("loaded labels")

    # 创建txt保存目录
    savepth = os.path.join(args.labels, args.type)
    os.makedirs(savepth, exist_ok=True)

    for line in tqdm(lines):
        # 图像名
        name = line['name']
        labels = line['labels']
        imagePath = os.path.join(imageRootPath, name)
        # labelPath = imagePath.replace('jpg', 'txt')
        labelPath = os.path.join(savepth, name.replace('jpg', 'txt'))

        if not os.path.isfile(os.path.realpath(imagePath)):
            continue
        with open(labelPath, 'w') as file:
            # 遍历label
            for label in labels:
                cat = label['category']
                if cat in classes:
                    counter[cat] += 1
                    file.write(convertBdd100k2yolo(imagePath, label))

    print(counter)
