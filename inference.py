from ultralytics import YOLO
import cv2
from copy import deepcopy
from ultralytics.utils.plotting import Annotator, colors




def get_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--chkpt', help="checkpoint path for car", type=str, default='best_bdd.pt')
    parser.add_argument('-p', '--point', help="checkpoint path for car_light", type=str, default='best_light.pt')
    parser.add_argument('-s', '--source', help="image file path", type=str, default='test')
    parser.add_argument('--conf', help="show conf", action="store_true")
    parser.add_argument('--labels', help="show labels", action="store_true")

    return parser.parse_args()

args = get_args()


# Load a pretrained YOLOv8n model
model = YOLO(args.chkpt)
model_bl = YOLO(args.point)

source = args.source

# Classes(bdd100k)
#   0: car
#   1: bus
#   4: truck

# Classes(8x)
#   2: car
#   5: bus
#   7: truck

# Run inference on the source
results = model.predict(source, conf=0.3, iou=0.6, classes=[2, 5, 7])  # list of Results objects
# results = model.predict(source, conf=0.2, iou=0.6, classes=[0, 1, 4])  # list of Results objects


for i,r in enumerate(results):
    boxes = r.boxes.xyxy.cpu().tolist()
    # cls_id = r.boxes.cls.cpu().tolist()
    # pic = r.orig_img
    # abc = r.plot(labels=True,boxes=True)
    # cv2.imwrite(f"trush/{i}.jpg",abc)
    
    annotator = Annotator(
            deepcopy(r.orig_img),
            line_width=1,
            example=r.names)
    
    conf = args.conf
    labels = args.labels
    for d in reversed(r.boxes):
        box = d.xyxy.cpu().squeeze()
        c, conf, id = int(d.cls), float(d.conf) if conf else None, None if d.id is None else int(d.id.item())
        name = ('' if id is None else f'id:{id} ') + r.names[c]
        label = (f'{name} {conf:.2f}' if conf else name) if labels else None
        
        annotator.box_label(box, label, color=colors(c, True))
    
        roi = r.orig_img[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
        results_bl = model_bl.predict(roi, conf=0.1)

        for r_bl in results_bl:
            for bx in r_bl.boxes:
                box1 = bx.xyxy.cpu().squeeze()
                box1[0] += box[0]
                box1[2] += box[0]
                box1[1] += box[1]
                box1[3] += box[1]

                c1, conf1 = int(bx.cls), float(bx.conf) if conf else None
                name1 = ('' if name is None else f'id:{name} ') + r_bl.names[c1]
                label1 = (f'{name1} {conf:.2f}' if conf else name1) if labels else None
                annotator.box_label(box1, label1, color=colors(c1, True))
    abc = annotator.result()
    cv2.imwrite(f"{i}.jpg",abc)
                    
            
 
                    



        
    
    
    





