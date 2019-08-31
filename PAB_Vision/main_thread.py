from flask import Flask, render_template
import os
import threading , time
import cv2
import numpy as np

def webcamCap(stop):
    cap = cv2.VideoCapture("http://192.168.43.102:4747/mjpegfeed")
    while(True):
        ret , frame = cap.read()
        #   RGB -> Grey Conversion (Optional)
        try:
            frame = frame[50: , 50:]
        except:
            pass

        cv2.imshow('Grey SelfCam' , frame)
        
        if stop():
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()