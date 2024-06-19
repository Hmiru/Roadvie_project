#Functions
import torch
import os
from PIL import Image
import shutil

def makelabel(model, image_path,label_path,size=1024):
    results = model(image_path, size)
    re = results.pandas().xyxy[0]
    re[re['name'] == 'ri']
    ri_rows = re[re['name'] == 'ri'].reset_index(drop=True)

    ri_rows.index = [0] * len(ri_rows)
    ri_rows_ = ri_rows[['xmin','ymin','xmax','ymax']]
    ri_rows_
    txt_filename = label_path[:-4] + '.txt'
    ri_rows_.to_csv(txt_filename, header=False, index=True, sep=' ')

def inpaint_object(image_path, label_info, fill_color=(255,255,255)):
    image = Image.open(image_path)
    width, height = image.size
    init = 0
    for line in label_info:
        label, left, bottom, right, top = map(float, line.split())

        if init==0:
            for i in range(0,height):
                for j in range(0,height):
                    image.putpixel((j, i), (0,0,0))
        if int(label) == 0:
            left = int(left)
            top = int(top)
            right = int(right)
            bottom = int(bottom)

        for i in range(bottom, top):
            for j in range(left, right):
                if not (0 <= i < height and 0 <= j < width):
                    continue
                image.putpixel((j, i), fill_color)
        init = init+1

    return image

def convert_jpg_to_png(input_folder):

    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith(".jpg"):
            input_path = os.path.join(input_folder, file_name)
            output_path = os.path.join(input_folder, os.path.splitext(file_name)[0] + ".png")

            with Image.open(input_path) as img:
                img.save(output_path, "PNG")

            os.remove(os.path.join(input_folder, file_name))

def copy_png_files(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for file_name in os.listdir(source_folder):
        if file_name.endswith(".png"):
            source_path = os.path.join(source_folder, file_name)
            destination_path = os.path.join(destination_folder, file_name)
            shutil.copyfile(source_path, destination_path)