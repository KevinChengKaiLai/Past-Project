import cv2
from ultralytics import YOLO

def main():
    print('hello')

    cap = cv2.VideoCapture(0)
    #model = YOLO('yolov8n.pt')
    model = YOLO('runs/detect/train4/weights/best.pt')
    while True:
        ret, frame = cap.read()
        result = model(frame,show=True,conf= 0.2)

        if (cv2.waitKey(30) ==27):
            break


if __name__ == "__main__":
    main()