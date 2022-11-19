# Get the libraries we need to run the program
import numpy as np  # numpy
import cv2 as cv    # OpenCV
import torch        # PyTorch
import serial       # Serial Comm
import time 


# Arduino setup
arduino = serial.Serial(port='COM8', baudrate=115200, timeout=.1)
currX = 0

# Serial Comm with Arduino
def write_read(x):
    data = ""
    try:
        arduino.write(bytes(x, 'utf-8'))
        time.sleep(0.01)
        data = arduino.readline()
    except:
        print("An exception occurred")
    
    return data



# Get input from device 0 (the webcam)
CAMERA_DEVICE_NUM = 0

# Download YOLOv5 machine learning model from PyTorch Hub
model = torch.hub.load('ultralytics/yolov5', 'yolov5x')

# Get the webcam video capture stream
#capture = cv.VideoCapture(CAMERA_DEVICE_NUM)
URL = "http://192.168.0.222"
capture = cv.VideoCapture(URL + ":81/stream")



# Get Video frame size :
width  = capture.get(cv.CAP_PROP_FRAME_WIDTH)   # float `width`
height = capture.get(cv.CAP_PROP_FRAME_HEIGHT)  # float `height`
# or
#width  = capture.get(3)  # float `width`
#height = capture.get(4)  # float `height`

print('width, height:', width, height)



# For every frame in the image...
while capture.isOpened():
    ret, frame = capture.read()

    # End the program if we didn't get a new frame
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
        
    # Use the model to run a prediction on the frame
    results = model(frame, size=640)

    # Get the prediction results and format them
    result_img = np.array(results.render())
    result_img = np.squeeze(result_img)



    if len(results) > 0:
        boxCoord =  results.pandas().xyxy[0]

        if len(boxCoord):
            midX =  boxCoord._get_value(0, 'xmin') + (boxCoord._get_value(0, 'xmax') - boxCoord._get_value(0, 'xmin')) / 2
            midY =  boxCoord._get_value(0, 'ymin') + (boxCoord._get_value(0, 'ymax') - boxCoord._get_value(0, 'ymin')) / 2

            print(str(midX) + " > " + str(midY))

            # Draw circle in middle :
            result_img = cv.circle(frame, (int(midX), int(midY)), int(2), (255,0,0), 2)


            # Check for abrupt increase :
            sensitivity = 10;

            if (midX < midX + sensitivity):

                # Rotate camera
                if int(midX > width/2) and currX >= 0:
                    currX = currX - 1
                    value = write_read(str(currX))

                elif int(midX < width/2) and currX <= 180:
                    currX = currX + 1
                    value = write_read(str(currX))
                

                print(">>> " + str(currX))

    # Show the results on screen
    cv.imshow('YOLOv5 Tracking demo', result_img)

    
    # Allow the program to be quit using the 'q' key
    if cv.waitKey(1) & 0xFF == ord('q'):
        break