import os
import shutil
import random

src_folder_path = "C:\\Users\\mirun\\image_ds\\roadview_dataset\\test_by_angle\\unlabeled"
dst_folder_path = "C:\\Users\\mirun\\image_ds\\roadview_dataset\\for_yolo"

# 파일 리스트 가져오기
all_files = os.listdir(src_folder_path)
image_files = [f for f in all_files if f.endswith('.png')]
txt_files = [f for f in all_files if f.endswith('.txt')]


labeled_images = []
for img in image_files:
    corresponding_txt = img.replace('.png', '.txt')
    if corresponding_txt in txt_files:

        labeled_images.append(img)
    else:
        print(f"Warning: No matching txt file for {img}. Leaving it in the current folder.")

# 파일을 무작위로 섞기
random.shuffle(labeled_images)

# 분할 지점 설정
num_files = len(labeled_images)
train_split = int(0.6 * num_files)
valid_split = train_split + int(0.2 * num_files)

# 폴더 생성
train_folder = os.path.join(dst_folder_path, 'train')
valid_folder = os.path.join(dst_folder_path, 'valid')
test_folder = os.path.join(dst_folder_path, 'test')
for folder in [train_folder, valid_folder, test_folder]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# 파일 이동
for i, img in enumerate(labeled_images):
    corresponding_txt = img.replace('.png', '.txt')
    if i < train_split:
        shutil.move(os.path.join(src_folder_path, img), train_folder)
        shutil.move(os.path.join(src_folder_path, corresponding_txt), train_folder)
    elif i < valid_split:
        shutil.move(os.path.join(src_folder_path, img), valid_folder)
        shutil.move(os.path.join(src_folder_path, corresponding_txt), valid_folder)
    else:
        shutil.move(os.path.join(src_folder_path, img), test_folder)
        shutil.move(os.path.join(src_folder_path, corresponding_txt), test_folder)
