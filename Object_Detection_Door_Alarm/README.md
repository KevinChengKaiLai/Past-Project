
# Object Detection : Safety Alarm
YOLOV8 object detection is the most popular algorithms nowadays,
today I am going to train on my own dataset to design a detection
of whether my door is opened or not for safety consideration.
The detection is perform by webcam of my computer.

## Video Demo <https://www.youtube.com/watch?v=ohZ6uxhO42g>



## Training Own Dataset with YOLOv8

The dataset comes from my iphone camera and the screenshot from my computers. Which is the photo include my door with two situations, opened or closed.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Preparing Your Dataset](#preparing-your-dataset)
3. [Configuring YOLOv8 for Custom Training](#configuring-yolov8-for-custom-training)
4. [Training Your Model](#training-your-model)
5. [Evaluating Your Model](#evaluating-your-model)

## Prerequisites

1. Install Python 3.6 or higher.
2. install YOLOV8 package:
pip3 install ultralytics

## Preparing Your Dataset

1. **Format Your Annotations**: Ensure that your dataset annotations are in the YOLO format. Each image's annotation should be in a separate `.txt` file with the same name as the image. The format is:
   ```
   [class] [x_center] [y_center] [width] [height]
   ```
       **Tips**: there is a lot of useful AI tool for annotations. For me, I used Makesense ai to do the annotation. Just google it!

2. **Organize Your Dataset**: Your dataset directory should be organized as:
   ```
   /train
       /images
           a.jpg
           b.jpg
           ...
       /labels
           a.txt
           b.txt
           ...
    /val
       /images
           a.jpg
           b.jpg
           ...
       /labels
           a.txt
           b.txt
           ...
   ```

3. **Split Your Dataset**: Make sure to split your data into training and validation sets. Place the images and their corresponding labels in their respective directories.

## Configuring YOLOv8 for Custom Training

1. **Modify Configuration File**: Duplicate one of the existing `.yaml` files in the `models` directory and modify it according to your needs. Update the number of classes and anchors if necessary. ex. data.yaml


### the file should looks like:
```
path: /the/path/before/your/train_and_val
train: ./train
val: ./val
test: ./test
nc: 2
names: ['Door Close', "Door Open"]
```
## Training Your Model

1. **Start the Training Process**:
   ```bash
    # Load a model
    model = YOLO('yolov8n.yaml')  # load untrained model
    # Train the model
    results = model.train(data='data.yaml', epochs=100, imgsz=1280, patience = 50 )

   ```

## Evaluating Your Model

1. Once training is complete, evaluate your model's performance on the validation set:
   ```bash
    import cv2
    from ultralytics import YOLO

    def main():
        cap = cv2.VideoCapture(0) #webcam
        model = YOLO('runs/detect/train/weights/last.pt')
        #here you have to change the 'train' text into any you like to apply like 'train6'
        #the defult directory of where model are placed
        while True:
            ret, frame = cap.read()
            result = model(frame, show = True, conf = 0.2)
            #show = True can visualize the box of detection
            if (cv2.waitKey(30) ==27): #if press 'q' can't stop the program, ctrl c is your friend!
                break

    if __name__ == "__main__":
        main()
   ```

2. Review the output for metrics such as confusion matrix to assess the quality of your trained model.

---

I hope this guide helps you train your custom dataset with YOLOv8. If you encounter any issues, please refer to the official YOLOv8 documentation or GitHub repository for further assistance.

---
