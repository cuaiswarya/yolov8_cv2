import random
import time
import sys
import pandas as pd
import datetime
import cv2
import numpy as np
from ultralytics import YOLO

import pymongo
from pymongo import MongoClient
client = pymongo.MongoClient("mongodb+srv://aunni:12345@cluster0.obaxokc.mongodb.net/")
db = client['Cluster0']
collection = db['Trial']

# opening the file in read mode
my_file = open("utils/coco.txt", "r")
# reading the file
data = my_file.read()
# replacing end splitting the text | when newline ('\n') is seen.
class_list = data.split("\n")
my_file.close()
df = pd.DataFrame(columns=['Time', 'Frame', 'Class_id', 'Confidence', 'Box'])
# Set the properties for the output video
frame_width = 1280
frame_height = 720
fps = 30
output_file = "output.mp4"


# print(class_list)

# Generate random colors for class list
detection_colors = []
for i in range(len(class_list)):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    detection_colors.append((b, g, r))

# load a pretrained YOLOv8n model
model = YOLO("weights/best_2.pt", "v8")

#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("videos/sample.mp4")

writer = None
start = time.time_ns()
frame_count = 0
total_frames = 0
fps = -1

bbs = []
confs = []
class_names = []
#clsIDs = []
times = []
frame_counts = []

bbs_temp = []


if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    _, frame = cap.read()
    if frame is None:
        print("End of stream")
        break
    # if frame is read correctly ret is True

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break



    #  resize the frame | small frame optimise the run
    # frame = cv2.resize(frame, (frame_wid, frame_hyt))
    frame_count += 1
    total_frames += 1
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    fps_label = "frame count: %.2f" % total_frames
    cv2.putText(frame, fps_label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2) 

    # Predict on image/video
    detect_params = model.predict(source=[frame], conf=0.3, save=False)

    # Convert tensor array to numpy
    DP = detect_params[0].numpy()
    #print(DP)
    
    if len(DP) != 0:

        for i in range(len(detect_params[0])):
            #print(i)
            boxes = detect_params[0].boxes
            box = boxes[i]  # returns one box
            clsID = box.cls.numpy()[0]
            conf = box.conf.numpy()[0]
            bb = box.xyxy.numpy()[0]
            class_name = class_list[int(clsID)]
           # print(conf, bb, class_name, total_frames)

           #define anarray named existingclassname n push class name replace bbs_temp with array name
            if class_name not in bbs_temp:
             bbs.append(bb)
             confs.append(conf)
                #clsIDs.append(clsID)
             class_names.append(class_name)
             times.append(current_time)
             frame_counts.append(total_frames)
             bbs_temp.append(class_name)

        
            cv2.rectangle(
                frame,
                (int(bb[0]), int(bb[1])),
                (int(bb[2]), int(bb[3])),
                detection_colors[int(clsID)],
                3,
            )
    
            # Display class name and confidence
            font = cv2.FONT_HERSHEY_COMPLEX
            cv2.putText(
                frame,
                class_list[int(clsID)] + " " + str(round(conf, 3)) + "%",
                (int(bb[0]), int(bb[1]) - 10),
                font,
                1,
                (255, 255, 255),
                2,
            )
            #save detected image
            #name = 'runs/detect/frame' + str(frame_count) + '.jpg'
            #print ('Creating...' + name)
            #cv2.imwrite(name, frame)

            df = pd.DataFrame({'Time' : times, 'Frame' : frame_counts, 'Class_name' : class_names, 'Confidence' : confs}) 
            df.to_csv('result.csv', index = False) 

            # Convert the DataFrame to a list of dictionaries
            #yolo_results = df.to_dict(orient='records')
            # Insert the list of documents into MongoDB
            #result = collection.insert_many(yolo_results)
            # Print the inserted document IDs
            #print("Inserted document IDs:", result)

'''# Initialize the video writer object
    if writer is None:
        resultVideo = cv2.VideoWriter_fourcc(*'mp4v')

        # Writing current processed frame into the video file
        writer = cv2.VideoWriter('result-video.mp4', resultVideo, fps = 30,frameSize = (1280,720))            

    # Write processed current frame to the file
    writer.write(frame)'''

    # Display the resulting frame
   # cv2.namedWindow("ObjectDetection", cv2.WINDOW_NORMAL)
    #cv2.imshow("ObjectDetection", frame)
    # Terminate run when "Q" pressed
   # if cv2.waitKey(1) == ord("q"):
   #    break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
#df = pd.DataFrame({'Time' : times, 'Frame' : frame_counts, 'Class_name' : class_names, 'Confidence' : confs}) 
#df.to_csv('result.csv', index = False) 
