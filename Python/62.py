import os

folder = 'd:\\Новая папка\\It Lager\\PDP School\\Python'
file_name = '61.py'
file_path = os.path.join(folder, file_name)

if os.path.exists(file_path):
    with os.scandir(os.getcwd()) as file_scan:
        for entry in file_scan:
            if entry.is_file():
                info = entry.stat()
                print(f"{entry.name} -> {info.st_mtime}, Size: {info.st_size} bytes")