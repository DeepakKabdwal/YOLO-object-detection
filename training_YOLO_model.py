#run this only once this is needed to get YOLOv8 from their repository
# import subprocess
# repo_url = 'https://github.com/ultralytics/ultralytics.git'
# clone_dir = './YOLOv8'
# subprocess.run(["git", "clone", repo_url, clone_dir])
import os
import random
from ultralytics import YOLO
import multiprocessing as mp
if __name__ == '__main__':
    mp.set_start_method('spawn')


model = YOLO('yolov8n.pt')
test_folder = "C:/Users/ACER/PycharmProjects/Yolo-object-detection/dataset\\test\\"



img_list = os.listdir(test_folder)
img_file = random.choice(img_list)
img_path = test_folder + img_file


# Run detection on selected image
results = model(img_path)

# Print detection results
results.show()


