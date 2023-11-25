import os
import imageio

def save_frames(video_path, output_folder, start_time, end_time):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    try:
        # Загрузка видео с использованием imageio
        video = imageio.get_reader(video_path, 'ffmpeg')

        fps = video.get_meta_data()['fps']
        start_frame = int(start_time * fps)
        end_frame = int(end_time * fps)

        total_frames = len(video)

        for frame_num in range(start_frame, min(end_frame, total_frames)):
            try:
                frame = video.get_data(frame_num)
            except IndexError:
                print(f"Видео {video_path}: Не удалось получить данные для кадра {frame_num}")
                break

            image_name = f"frame_{frame_num}.jpg"
            image_path = os.path.join(output_folder, image_name)

            # Добавляем уникальный индекс к имени файла, если файл уже существует
            index = 0
            while os.path.exists(image_path):
                index += 1
                image_name = f"frame_{frame_num}_{index}.jpg"
                image_path = os.path.join(output_folder, image_name)

            # Сохраняем кадр в виде изображения
            imageio.imwrite(image_path, frame)
            print(f"Кадр {image_name} успешно сохранен")
    except Exception as e:
        print(f"Произошла ошибка при обработке видео {video_path}: {str(e)}")

# Параметры времени
start_time = 20  # начало отрезка (в секундах)
end_time = 22  # конец отрезка (в секундах)

# Путь к вашим папкам
base_folder = './data_cut'

# Обход каждой папки
for class_label, folder_name in enumerate(['Бетон', 'Грунт', 'Дерево', 'Кирпич']):
    class_label += 1  # начинаем с 1, так как у вас классы с 1 по 4

    video_folder = os.path.join(base_folder, folder_name)
    output_folder = os.path.join('./dataset_classification', folder_name)

    print(f"Обработка папки {video_folder}...")

    # Обработка каждого видео в папке
    for video_name in os.listdir(video_folder):
        video_path = os.path.join(video_folder, video_name)
        print(f"Обработка видео {video_name}...")
        save_frames(video_path, output_folder, start_time, end_time)

print("Готово!")
