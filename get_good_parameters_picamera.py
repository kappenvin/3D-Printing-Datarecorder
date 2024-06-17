from picamera2 import Picamera2
import sys
import neopixel_spi as neopixel
import board
import time


NUM_PIXELS = 8
PIXEL_ORDER = neopixel.GRB
COLORS = (0xFF0000, 0x00FF00, 0x0000FF)
DELAY = 0.1

spi = board.SPI()


pixels = neopixel.NeoPixel_SPI(spi,
                               NUM_PIXELS,
                               pixel_order=PIXEL_ORDER,
                               brightness=1.0,
                               auto_write=False)
pixels[1]=0xFFFFFF
pixels[2]=0xFFFFFF
pixels[3]=0xFFFFFF
pixels[4]=0xFFFFFF
pixels[5]=0xFFFFFF
pixels[6]=0xFFFFFF
pixels.show()



picam2 = Picamera2()
config=picam2.create_still_configuration(main={"size": (1720, 1280)},controls={"ExposureTime": 10000})

picam2.configure(config)
#print(picam2.camera_controls)
#print(picam2.sensor_modes)
#picam2.configure(picam2.create_preview_configuration())
#picam2.set_controls({"ExposureTime": 5000})
time.sleep(2)

picam2.start()
picam2.capture_file("test_new_1.0_bright_3000_exp.jpg")


pixels.fill(0)
pixels.show()

sys.exit()
picam2.set_controls({"ExposureTime": 10000, "AnalogueGain": 1.0})
picam2.start()
