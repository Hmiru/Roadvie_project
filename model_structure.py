import torch

# Model
model = torch.hub.load('yolov5', 'yolov5s', pretrained=True)

# Image
img = 'https://ultralytics.com/images/zidane.jpg'

# Inference
results = model(img)