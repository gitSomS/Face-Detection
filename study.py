import cv2, os
import numpy as np
from PIL import Image
import pickle
import sqlite3

#recognizer = cv2.createLBPHFaceRecognizer()
faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#path = 'dataSet'

def getProfile(id):
    conn = sqlite3.connect("FaceBase.db")
    cmd = "SELECT * FROM People WHERE ID="+str(id)
    cursor = conn.execute(cmd)
    profile = None
    for row in cursor:
        profile = row
    conn.close()
    return profile

cam = cv2.VideoCapture(1)
#font = cv2.InitFont(cv2.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1,)
while True:
    ret, im = cam.read()
    gray = cv2. cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces= faceDetectdetectMultiSacale(gray, 1.3,5))
    for (x,y,w,h) in faces:
        sampleNum=sampleNum+1
        id, conf = recognizer. predict (gray[y:y+h,x:x+w])
        cv2.imwrite("cctv_rostos"+str(id)+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
        cv2.rectangle(im, (x,y), (x+w, y+h), (255,0,00),2)
        profile=getProfile(id)
        if(profile!=None):
            cv2.cv.putText(cv2.cv.fromarray(im),str(profile[1]),(x,y+h+30),font, 255)
            cv2.cv.putText(cv2.cv.fromarray(im),str(profile[2]),(x,y+h+60),font, 255)
            cv2.cv.putText(cv2.cv.fromarray(im),str(profile[3]),(x,y+h+90),font, 255)
            cv2.cv.putText(cv2.cv.fromarray(im),str(profile[4]),(x,y+h+120),font, 255)       
        cv2.imshow("im", im)
        cv2.waitKey(10)