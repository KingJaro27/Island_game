import os
from PIL import Image

def rename_images_in_folder(folder_path):
    files = os.listdir(folder_path)
    
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    image_files = [f for f in files if os.path.splitext(f)[1].lower() in image_extensions]
    
    image_files.sort()
    
    for index, image_file in enumerate(image_files):
        new_name = f"{index}{os.path.splitext(image_file)[1]}"
        new_path = os.path.join(folder_path, new_name)
        old_path = os.path.join(folder_path, image_file)
        os.rename(old_path, new_path)
        print(f"Renamed {old_path} to {new_path}")

folder_path = "data/Boss/Walk"
rename_images_in_folder(folder_path)