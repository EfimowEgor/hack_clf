import os

import cv2

def cut_video(input_path, output_path, start_time, end_time):
    try:
        # Открытие видеофайла
        cap = cv2.VideoCapture(input_path)

        # Проверка, удалось ли открыть файл
        if not cap.isOpened():
            print("Ошибка открытия видеофайла")
            return

        # Определение параметров видео
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Расчет кадров для начала и конца отрезка
        start_frame = int(start_time * fps)
        end_frame = int(end_time * fps)

        # Переход к начальному кадру
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        # Создание объекта для записи видео
        fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Выберите подходящий кодек
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        # Обработка кадров в выбранном временном диапазоне
        for frame_num in range(start_frame, end_frame):
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)

        # Закрытие файлов и освобождение ресурсов
        cap.release()
        out.release()
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"Ошибка при обработке видео {input_path}: {str(e)}")

if __name__ == "__main__":
    input_dir = "./data/Кирпич"
    out_dir = "./data_cut/Кирпич"
    input_vids = os.listdir(input_dir)

    start_time, end_time = 110, 135

    for vid in input_vids:
        print(vid)
        f = os.path.join(input_dir, vid)
        o = os.path.join(out_dir, vid)

        cut_video(f, o, start_time, end_time)
