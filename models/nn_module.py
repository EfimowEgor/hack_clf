from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
import cv2
import torch
from torchvision import transforms
from PIL import Image
import argparse
import imageio
import os
from collections import Counter
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--path", help="Path to video")
    group.add_argument("--dir", help="Path to folder with videos")

    args = parser.parse_args()

    return args

class Transform:
    def __init__(self, vid_path):
        self.vid_path = vid_path
        self.start = 60 + 50 + 17
        self.end = 60 + 50 + 22
        self.frames = []
    
    def framing(self):
        # Раскадровка полученного промежутка видео и последующая передача его в Yolo
        video = imageio.get_reader(self.vid_path, 'ffmpeg')

        fps = video.get_meta_data()['fps']
        start_frame = int(self.start * fps)
        end_frame = int(self.end * fps)

        total_frames = len(video)

        for frame_num in range(start_frame, min(end_frame, total_frames)):
            try:
                frame = video.get_data(frame_num)
                self.frames.append(frame)
            except IndexError:
                print(f"Видео {self.vid_path}: Не удалось получить данные для кадра {frame_num}")
                break

class YoloViTModule:
    # Yolo не смог прикрутить, будет классическая классификация :(
    def __init__(self, path_to_vit_weights):
        self.classes = {0: "Бетон",
                        1: "Грунт",
                        2: "Дерево",
                        3: "Кирпич"}
        # self.yolo = YOLO(path_to_yolo_weights)
        self.vit = torch.load(path_to_vit_weights, map_location="cpu")
        self.vit.eval()
        self.test_transforms = transforms.Compose(
            [
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
            ]
        )
    
    def predict(self, img_path):
        # image = Image.open(img_path).convert("RGB")
        image = Image.fromarray(img_path)
        image = self.test_transforms(image)
        image = image.unsqueeze(0)
        res = self.vit(image)
        return res
            

if __name__ == "__main__":
    model = YoloViTModule("./models/weights/checkpoint.pth")

    label2idx = {"Бетон": 1,
                 "Грунт": 3,
                 "Дерево": 2,
                 "Кирпич": 4}

    args = parse_args()

    if args.path:
        transfromer = Transform(args.path)
        transfromer.framing()

        rs = model.predict(transfromer.frames[0])
        predicts = []
        for frame in transfromer.frames:
            predicts.append(model.classes[torch.argmax(model.predict(frame)).item()])

        counter = Counter(predicts).most_common()[0]
        
        # Добавляем Hard Voting
        print(f"Classification result: {counter[0]}")
    elif args.dir:
        videos = os.listdir(args.dir)
        file_names = []
        labels = []
        for video in videos:
            transfromer = Transform(os.path.join(args.dir, video))
            transfromer.framing()

            rs = model.predict(transfromer.frames[0])
            predicts = []
            for frame in transfromer.frames:
                predicts.append(model.classes[torch.argmax(model.predict(frame)).item()])

            counter = Counter(predicts).most_common()[0]
            print(f"{video} --- Classification result: {counter[0]}")
            file_names.append(video)
            labels.append(label2idx[counter[0]])
            df = pd.DataFrame({
                "video_filename":file_names,
                "class": labels
            })
            df.to_csv("submission.csv", index=False, sep=";")