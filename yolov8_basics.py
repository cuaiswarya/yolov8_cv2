from ultralytics import YOLO
import numpy

# load a pretrained YOLOv8n model
model = YOLO("bestv8.pt", "v8")  

# predict on an image
detection_output = model.predict(source="inference/videos/VIDEO_TO_ELABORATE_1.MOV", conf=0.25, save_txt=True) 
#python detect.py --weights bestv8.pt --save-txt det.txt


# Display tensor array
print(detection_output)

# Display numpy array
print(detection_output[0].numpy())
