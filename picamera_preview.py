from picamera2 import Picamera2, Preview
import time
from datetime import datetime
import os 

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration(main={"size": (1720, 1280)})
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
picam2.start()
time.sleep(100)