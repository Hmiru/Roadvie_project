import shutil
import os
import re

output_path='C:/Users/mirun/PycharmProjects/Roadview_project/Roadview_project/lama/data/output'
return_path="C:/Users/mirun/PycharmProjects\Roadview_project/Roadview_project/raw_data/test/test_3"


for root, dirs, files in os.walk(output_path):
    for file in files:
        cleaned_filename = re.sub(r'_mask', '', file)
        pattern = re.compile(r'(img\d+)_([a-d])_')
        match = pattern.search(file)
        if match:
            img_number = match.group(1)
            letter = match.group(2)
            photo_directory=os.path.join(return_path,img_number,letter)
            if not os.path.exists(photo_directory):
                os.makedirs(photo_directory)
            original_file_path=os.path.join(root, file)
            shutil.move(original_file_path,photo_directory)




