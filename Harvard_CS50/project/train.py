from ultralytics import YOLO
print('hello')
# Load a model
model = YOLO('yolov8n.yaml')  # load a pretrained model (recommended for training)

# Train the model with 2 GPUs
results = model.train(data='data.yaml', epochs=100, imgsz=1280, patience = 50 )
