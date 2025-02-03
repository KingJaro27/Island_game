import os
from PIL import Image

def rename_images_in_folder(folder_path):
    # Liste aller Dateien im Ordner
    files = os.listdir(folder_path)
    
    # Filtere nur Bilddateien (kannst du erweitern, um andere Formate zu unterstützen)
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    image_files = [f for f in files if os.path.splitext(f)[1].lower() in image_extensions]
    
    # Sortiere die Bilddateien nach Namen
    image_files.sort()
    
    # Benenne die Bilder um
    for index, image_file in enumerate(image_files):
        # Erstelle den neuen Dateinamen
        new_name = f"{index}{os.path.splitext(image_file)[1]}"
        new_path = os.path.join(folder_path, new_name)
        
        # Umbenennen der Datei
        old_path = os.path.join(folder_path, image_file)
        os.rename(old_path, new_path)
        print(f"Renamed {old_path} to {new_path}")

# Beispielaufruf
folder_path = "data/Trader_3/Idle_2"
rename_images_in_folder(folder_path)