import torch
import os

from funct import makelabel, inpaint_object, convert_jpg_to_png, copy_png_files

#0
image_folder = "raw_data\\images"
label_folder = "raw_data\\label_yolo"
mask_folder = "raw_data\\mask"
lama_folder = "lama\\data\\input"

#1
model = torch.hub.load('yolov5', 'custom', path='yolov5/runs/best1024.pt', source='local')  # local repo
if not os.path.exists(label_folder):
    os.makedirs(label_folder)

for filename in os.listdir(image_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(image_folder, filename)
        label_path = os.path.join(label_folder, filename)
        makelabel(model, image_path,label_path)

#2
label_files = os.listdir(label_folder)
label_files.sort()
for label_file in label_files:
    with open(os.path.join(label_folder, label_file), 'r') as f:
        label_info = f.readlines()
    image_name = label_file.rsplit('.', 1)[0] + '.png'
    mask_name = label_file.rsplit('.', 1)[0] + '_mask.png'
    image_path = os.path.join(image_folder, image_name)

    output_image = inpaint_object(image_path, label_info)

    output_dir = 'raw_data/mask'
    os.makedirs(output_dir, exist_ok=True)
    output_image.save(os.path.join(output_dir, mask_name))

#3
convert_jpg_to_png(image_folder)
convert_jpg_to_png(mask_folder)
#4
copy_png_files(image_folder, lama_folder)
copy_png_files(mask_folder, lama_folder)