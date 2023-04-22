from ultralytics import YOLO
from multiprocessing import freeze_support

if __name__ == '__main__':
    freeze_support()
    model = YOLO('yolov8s.yaml')
    model.train(data="C:\\Users\\ACER\\PycharmProjects\\Yolo-object-detection\\data.yaml", epochs=50)
