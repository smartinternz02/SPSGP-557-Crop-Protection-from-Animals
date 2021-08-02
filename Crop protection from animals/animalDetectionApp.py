# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 17:21:31 2021

@author: Anushka
"""


# -*- coding: utf-8 -*-
import cv2
from flask import Flask, render_template, Response
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import winsound

app = Flask(__name__)

animalFound =""

model = load_model("smartbridge.h5")
Animal_List = ["Butterfly","Cat","Chicken","Cow","Dog","Elephant","Horse","Sheep","Spider","Squirrel"]
"""
here we would initilize/load our model 


"""
#configuring the inputs and detection
##load the input video
### initializing our video stream


def gen():
    print("[INFO] accessing video stream...")
    cap = cv2.VideoCapture(r"E:\SmartInternz\Project\Crop_Protection_from_Animals\test\ele_dog.mp4")
    size=4
    while True:
        if cap.grab():
            flag, frame = cap.retrieve()
        if not flag:
            continue
        else:
            cv2.imwrite("1.jpg",frame)
            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')
            a = cv2.resize(frame,(299,299))   
            normalized=a/255.0
            normalized = cv2.flip(normalized,1,1)
            mini = cv2.resize(normalized, (normalized.shape[1] // size, normalized.shape[0] // size))
            x = image.img_to_array(normalized)
            x = np.expand_dims(x,axis=0)
            b = np.argmax(model.predict(x))
            cv2.putText(frame,Animal_List[b], (100, 100),cv2.FONT_HERSHEY_TRIPLEX ,1.75, (255,255,255), 2)
            cv2.imwrite("1.jpg",frame)
            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')
            if(Animal_List[b] != "Butterfly" and Animal_List[b] != "Spider" and Animal_List[b] != "Squirrel"):
                #playsound('cut-alert.mp3')
                animalFound = "Alert!!! Animal Found"
                frequency = 2500  # Set Frequency To 2500 Hertz
                duration =  5000  # Set Duration To 1000 ms == 1 second
                winsound.Beep(frequency, duration)
                break
                

            #cv2.imshow('video', frame)
            
            if cv2.waitKey(5) == 27:
                break
    cap.release()

# Close all started windows
    cv2.destroyAllWindows()

##configuring our home page
@app.route('/')
def index():
    return render_template('index.html',animal_found= animalFound)

#route for video feed
@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')
   
if __name__ == '__main__':
    app.run(debug = True, threaded = False)