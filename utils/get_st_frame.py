import os
import cv2

def extract_first_frame(video_path, output_dir, idx):
    # Открытие видеофайла
    cap = cv2.VideoCapture(video_path)

    # Проверка, удалось ли открыть файл
    if not cap.isOpened():
        print("Ошибка открытия видеофайла")
        return

    # Чтение первого кадра
    ret, frame = cap.read()

    # Проверка, удалось ли прочитать первый кадр
    if not ret:
        print("Ошибка чтения первого кадра")
        return

    # Сохранение первого кадра в формате JPEG
    output_path = os.path.join(output_dir, f"image{idx}.jpg")
    cv2.imwrite(output_path, frame)

    # Закрытие файлов и освобождение ресурсов
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_paths = ["./data_cut/Бетон", "./data_cut/Грунт", "./data_cut/Дерево", "./data_cut/Кирпич"]
    output_dir = "./data_st_frame"

    cnt = 0

    for path in video_paths:
        for vid in os.listdir(path):
            video_path = os.path.join(path, vid)
            extract_first_frame(video_path, output_dir, cnt)
            cnt += 1
