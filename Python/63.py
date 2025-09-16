import os
import shutil
from datetime import datetime

def delete_all_files(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Xato yuz berdi: {e}")

current_date = datetime.now()
year = current_date.year
month = current_date.month
day = current_date.day

for i in range(1, 4): 
    folder_name = f"Catalog_{year}_{month}_{day}_No_{i}"
    os.makedirs(folder_name)

source_folders = ["Catalog_2024_2_5_No_1", "Catalog_2024_2_5_No_2", "Catalog_2024_2_5_No_3"]
destination_folder = "Nusxalar"

for source_folder in source_folders:
    source_path = os.path.abspath(source_folder)
    destination_path = os.path.join(os.path.abspath(destination_folder), os.path.basename(source_folder))
    shutil.copytree(source_path, destination_path)

print("Amallar muvaffaqiyatli bajarildi.")
