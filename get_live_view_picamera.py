import sys 
import time
import requests
import threading
from datetime import datetime
import os
import qwiic_kx13x
import csv
from picamera2 import Picamera2, Preview

def save_images_picamera():

    # check if the could be accessed
    picam2 = Picamera2()
    camera_config = picam2.create_preview_configuration()
    picam2.configure(camera_config)
    picam2.start_preview(Preview.QTGL)
    picam2.start()
    time.sleep(2)
    

    # get the image and save them 
    while True:
        if my_event.is_set():
            print("hello1")
            #picam2.stop_preview()
            picam2.close()
            break

my_event = threading.Event()
t1 = threading.Thread(target = save_images_picamera) # create t1 thread
#t2= threading.Thread(target = save_accelerometer,args=(slicer_settings_name,filename_final,))
t1.start()
time.sleep(5)
print("hello")
my_event.set()
#t1.join()
time.sleep(5)
print("hello")
my_event.clear() 
t1 = threading.Thread(target = save_images_picamera)
t1.start()
time.sleep(5)
my_event.set()
#t1.join() 

