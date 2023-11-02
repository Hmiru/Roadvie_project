
import os
import pandas
import torch
image_folder = "raw_data/images_not_true"
label_folder = "raw_data/label_yolo_not_true"
model = torch.hub.load('../yolov5', 'custom',
                       path='Roadview_project/yolov5/runs/train/exp7/weights/best.pt', source='local')  # local repo

def makelabel(model, image_path,label_path,size=1140):
    results = model(image_path, size)
    re = results.pandas().xyxy[0]
    ri_rows = re[re['name'] == 'text icon'].reset_index(drop=True)
    ri_rows.index = [0] * len(ri_rows)
    ri_rows_ = ri_rows[['xmin', 'ymin', 'xmax', 'ymax']]
    return ri_rows_

for filename in os.listdir(image_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(image_folder, filename)
        label_path = os.path.join(label_folder, filename)
        print(makelabel(model, image_path, label_path))