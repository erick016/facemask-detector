import os
import cv2
import numpy as np
import binascii
import serial
import time

check_flag = False

serialPort = serial.Serial(
    port="COM4", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
)

# Define paths
base_dir = os.path.dirname(__file__)
print(base_dir)
prototxt_path = os.path.join(base_dir + 'model_data/deploy.prototxt')
caffemodel_path = os.path.join(base_dir + 'model_data/weights.caffemodel')

# Read the model
model = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)

old_image_count = 0
image_count = 0

old_files = []
new_files = []

for file in os.listdir('Z:/DCIM/Camera'):
    android_file_name, android_file_extension = os.path.splitext(file)
    if (android_file_extension in ['.png','.jpg']):
        old_image_count += 1
    
    
    old_files.append(file)


print(old_files)


while check_flag == False:

    new_files = []
    
    for file in os.listdir('Z:/DCIM/Camera'):
        android_file_name, android_file_extension = os.path.splitext(file)
        if (android_file_extension in ['.png','.jpg']):
            image_count += 1
        #print(str(old_image_count) + "|" + str(image_count))
        
        new_files.append(file)


        
    if (image_count > old_image_count):
        old_image_count = image_count
        image_count = 0
        print(new_files)
        latest_file = list(set(new_files) - set(old_files))
        print(latest_file[0])
        old_files = new_files
        image = cv2.imread('Z:/DCIM/Camera/' + latest_file[0])


        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

        model.setInput(blob)
        detections = model.forward()

        #Identify each face
        for i in range(0, detections.shape[2]):
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            confidence = detections[0, 0, i, 2]

            if (confidence > 0.5):
                frame = image[startY:endY, startX:endX]
                content_grayscaled = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                content_resized = cv2.resize(content_grayscaled,(28,28))
                print(binascii.hexlify(content_resized))
                print('Confident.')



                serialString = serialPort.readline()            
                serialPort.write(binascii.hexlify(content_resized))

                while "pred label:" not in serialString.decode("Ascii"):

                    serialString = serialPort.readline()


                    try:
                        print(serialString.decode("Ascii"))
                    except:
                        pass
        
                check_flag = True 

            

    else:
        image_count = 0
        
        
