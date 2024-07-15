from picamera2 import Picamera2, Preview
import time
from datetime import datetime
import os 
import time
import board
import neopixel_spi as neopixel
import sys



NUM_PIXELS = 8
PIXEL_ORDER = neopixel.GRB
COLORS = (0xFF0000, 0x00FF00, 0x0000FF)
DELAY = 0.1

spi = board.SPI()


pixels = neopixel.NeoPixel_SPI(spi,
                            NUM_PIXELS,
                            pixel_order=PIXEL_ORDER,
                            brightness=0.5,
                            auto_write=False)


pixels[1]=0xFFFFFF
pixels[2]=0xFFFFFF
pixels[3]=0xFFFFFF
pixels[4]=0xFFFFFF
pixels[5]=0xFFFFFF


pixels.show()

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(camera_config)

picam2.set_controls({"FrameDurationLimits": (10000, 10000)})  # For 90fps, frame duration should be around 11ms

picam2.start_preview(Preview.QTGL)
picam2.start()
time.sleep(10)

pixels.fill(0)
pixels.show()

time.sleep(4)