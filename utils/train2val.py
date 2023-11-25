import os
import shutil

def copy_files_and_remove_source(source_folder, destination_folder, file_list_path):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    with open(file_list_path, 'r') as file:
        file_names = file.read().splitlines()

    for file_name in file_names:
        image_path = os.path.join(source_folder, file_name.replace("data/obj_train_data/", ""))
        txt_path = os.path.splitext(image_path)[0] + ".txt"

        destination_image_path = os.path.join(destination_folder, os.path.basename(image_path))
        destination_txt_path = os.path.splitext(destination_image_path)[0] + ".txt"

        source_folder_path = os.path.dirname(image_path)
        if not os.path.exists(source_folder_path):
            os.makedirs(source_folder_path)

        shutil.copy(image_path, destination_image_path)
        shutil.copy(txt_path, destination_txt_path)

        print(f"Копирование файла: {file_name}")
        print(f"Копирование файла: {os.path.basename(txt_path)}")

        # Удаление файлов из папки исходной
        os.remove(image_path)
        os.remove(txt_path)

        print(f"Удаление файла из папки исходной: {image_path}")
        print(f"Удаление файла из папки исходной: {txt_path}")

if __name__ == "__main__":
    source_folder = "./dataset_yolo/obj_train_data"
    destination_folder = "./dataset_yolo/obj_val_data"
    file_list_path = "./dataset_yolo/val.txt" 

    copy_files_and_remove_source(source_folder, destination_folder, file_list_path)
