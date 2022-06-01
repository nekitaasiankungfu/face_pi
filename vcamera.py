from unicodedata import name
from picamera import PiCamera
from picamera.array import PiRGBArray
import RPi.GPIO as GPIO
from time import sleep
import board
import busio as io
import adafruit_mlx90614
import cv2
import os
from db import Database

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('D:\\facerec_learn\\trainer\\trainer.yml')

#iniciate id counter
id = 0
# names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', 'Nikita', 'Taimas', 'Ilza', 'Z', 'W'] 

led_red = 22
led_green = 27
buzzer = 17

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led_red, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(led_green, GPIO.OUT, initial=GPIO.LOW)

def mape(x: float, in_min: float, in_max: float, out_min:float, out_max: float) -> float:
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
camera = PiCamera()
camera.resolution = (800, 480)
camera.rotation = 180
camera.framerate = 32
raw_capture = PiRGBArray(camera, size=(800, 480))
sleep(0.2)

i2c = io.I2C(board.SCL, board.SDA, frequency=100000)
mlx = adafruit_mlx90614.MLX90614(i2c)

face_cascade = cv2.CascadeClassifier("face_cascade.xml")
#body_cascade = cv2.CascadeClassifier("upperbody_cascade.xml")

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.namedWindow("TSensor", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("TSensor",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    image = frame.array
    faces = face_cascade.detectMultiScale(image, scaleFactor=1.5, minNeighbors=5, minSize=(20, 20))
    temp = round(mlx.object_temperature, 1)
    if temp >= 29.5 and temp <= 32.5: 
        temp_ = mape(temp, 29, 32.5, 32.5, 36.8)
        GPIO.output(led_green, GPIO.HIGH)
        GPIO.output(led_red, GPIO.LOW)
        os.system('mpg321 1.mp3 &')
    elif 38 >= temp >= 32.5:
        if (temp >32,5 and name):
         Database.InsertToDB(temp, name)
         Database.Commit()    
         temp_ = mape(temp, 32.5, 38, 36.9, 40)
         GPIO.output(led_red, GPIO.HIGH)
         GPIO.output(led_green, GPIO.LOW)
         os.system('mpg321 2.mp3 &')
    else:
        temp_ = temp
        GPIO.output(led_green, GPIO.LOW)
        GPIO.output(led_red, GPIO.LOW)

    cv2.putText(image, f"Temperature: {round(temp_, 1)} ",(20,450), font, 2, (255, 255, 255), 2, cv2.LINE_AA)
    
    for (x, y, w, h) in faces:       
        cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        # Check if confidence is less them 100 ==> "0" is perfect match 
        if (confidence > 30):
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
        
        cv2.putText(image, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(image, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
        
    cv2.imshow("TSensor", image)
    key = cv2.waitKey(1) & 0xFF
    raw_capture.truncate(0)
    if key == ord("q"):
        break

#export DISPLAY=":0"
#camera.start_preview()
#camera.capture("test1.jpg")
#sleep(5)
#camera.stop_preview()

#camera.rotation(90)
#camera.start_preview(alpha=200)
#camera.capture(filePath)
#camera.start_recording()
#camera.stop_recording()
#camera.resolution = (2592, 1944)
#camera.framerate = 15
#camera.annotate_text = "Hello world!"

# Camera Effects

#https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/7