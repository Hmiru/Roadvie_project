import torch
import os
import yaml
import shutil
from Roadview_project.my_code.define_functions import makelabel, inpaint_object, copy_png_files

with open('config.yaml', 'r',encoding='utf-8') as stream:
    config = yaml.safe_load(stream)

image_dataset_path = config['path']['image_dataset_path']
label_folder = config['path']['label_folder_path']
mask_folder = config['path']['mask_folder_path']
icon_detected_image_folder_path = config['path']['icon_detected_image_folder_path']
lama_folder = config['path']['lama_folder_path']

model = torch.hub.load('../yolov5', 'custom',
                       path='../yolov5/runs/train/exp9/weights/best.pt', source='local')  # local repo
if not os.path.exists(label_folder):
    os.makedirs(label_folder)

if not os.path.exists(icon_detected_image_folder_path):
    os.makedirs(icon_detected_image_folder_path)

for place_directory in os.listdir(image_dataset_path):
    place_directory_path = os.path.join(image_dataset_path,place_directory)

    for cluster_directory in os.listdir(place_directory_path):
        cluster_directory_path = os.path.join(place_directory_path, cluster_directory)

        for image_file in os.listdir(cluster_directory_path):
            if image_file.endswith(".jpg") or image_file.endswith(".png"):
                image_path = os.path.join(cluster_directory_path, image_file)
                label_filename = os.path.splitext(image_file)[0] + '.txt'
                label_path = os.path.join(label_folder, label_filename)

                makelabel(model, image_path, label_path)

                if os.path.exists(label_path):
                    with open(label_path, 'r') as f:
                        label_info = f.readlines()

                    mask_name = image_file.rsplit('.', 1)[0] + '_mask.png'

                    output_image = inpaint_object(image_path, label_info)
                    output_image.save(os.path.join(mask_folder, mask_name))

                    shutil.move(image_path, icon_detected_image_folder_path)


copy_png_files(icon_detected_image_folder_path, lama_folder)
copy_png_files(mask_folder, lama_folder)