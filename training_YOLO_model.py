#run this only once this is needed to get YOLOv8 from their repository
# import subprocess
# repo_url = 'https://github.com/ultralytics/ultralytics.git'
# clone_dir = './YOLOv8'
# subprocess.run(["git", "clone", repo_url, clone_dir])
import os
from ultralytics import YOLO
import multiprocessing as mp
if __name__ == '__main__':
    mp.set_start_method('spawn')


model = YOLO('yolov8n.yaml')
model.train(data='data.yaml', epochs=1)

