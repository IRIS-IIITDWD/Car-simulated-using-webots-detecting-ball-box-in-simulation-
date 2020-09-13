#!/home/yashprime1/anaconda3/bin/python3
#!pip3 install dnspython
#!pip3 install pymongo[srv]
#!pip3 install tensorfow
import os
import tensorflow as tf

from PIL import Image, ImageOps
import numpy as np
import io
from PIL import Image
import cv2

from controller import Robot
from controller import Keyboard
from controller import Camera

from bson.objectid import ObjectId
TIME_STEP = 64

EMOTIONS_LIST = ['BALL','EMPTY','BOX']    

model = tf.keras.models.load_model('keras_model.h5')
robot = Robot()
timestep = int(robot.getBasicTimeStep())

keyboard=Keyboard()
keyboard.enable(timestep)
lr=robot.getMotor('linear')
rm=robot.getMotor('RM')
cm=robot.getCamera('CAM')
cm.enable(TIME_STEP)
counter=0
wheels = []
wheelsNames = ['wheel1', 'wheel2', 'wheel3', 'wheel4']
for i in range(4):
    wheels.append(robot.getMotor(wheelsNames[i]))
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(0.0)
linear =0.0
rotate=0.0    
c=0
while robot.step(TIME_STEP) != -1:
    if c==0:
        k=ord('A')
    else:
        k=ord('W')    
    key=keyboard.getKey()
    leftSpeed = 0.0
    rightSpeed = 0.0

    if(k==ord('W')):
        leftSpeed = 1
        rightSpeed = 1
    elif(k==ord('S')):
        leftSpeed = -1
        rightSpeed = -1
    elif (k==ord('A')):
        leftSpeed = 1
        rightSpeed = -1
    elif(k==ord('D')):
        leftSpeed = -1
        rightSpeed = 1
    else:
        leftSpeed = 0.0
        rightSpeed = 0.0
    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(leftSpeed)
    wheels[2].setVelocity(rightSpeed)
    wheels[3].setVelocity(rightSpeed)
    if(key==ord('B') and linear<0.2):
        linear += 0.005
    elif(key==ord('C') and linear>-2):
        linear += -0.005
    else:
        linear += 0
    lr.setPosition(linear)
    if(key==ord('G') and rotate<1.57):
        rotate += 0.005
    elif(key==ord('V') and rotate >-1.57):
        rotate += -0.005
    else:
        rotate += 0
    rm.setPosition(rotate)
  
    counter
    #img=cm.getImageArray()
    cm.saveImage(str(counter)+'.jpg',100)
    img=cv2.imread((str(counter)+'.jpg')) 

    #print(type(image))
    img = cv2.resize(img, (224, 224))
    image_array=np.reshape(img,(1,224,224,3))
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1   
    prediction = model.predict(normalized_image_array)
    k=np.argmax(prediction)
    print(EMOTIONS_LIST[k])
    if EMOTIONS_LIST[k] == 'BALL':
        c=1   