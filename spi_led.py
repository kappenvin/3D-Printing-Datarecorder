import time
import board
import neopixel_spi as neopixel
import sys

# you have to install the lbraray following this github repository https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel_SPI

NUM_PIXELS = 8
PIXEL_ORDER = neopixel.RGBW
COLORS = (0xFF0000, 0x00FF00, 0x0000FF)
DELAY = 0.1

spi = board.SPI()


pixels = neopixel.NeoPixel_SPI(spi,
                               NUM_PIXELS,
                               pixel_order=PIXEL_ORDER,
                               brightness=1,
                               auto_write=False)

"""
pixels[0]=(255,0,0)
pixels.show()
time.sleep(2)
pixels[0]=(0,0,0)
pixels.show()
time.sleep(2)
"""
print("hallo")
pixels[1]=0xFFFFFF
pixels[2]=0xFFFFFF
pixels[3]=0xFFFFFF
#pixels[4]=0xFFFFFF
#pixels[5]=0xFFFFFF
#pixels[6]=0xFFFFFF
#pixels.fill(0xFFFFFF)
pixels.show()
print("hallo")
time.sleep(4)
pixels.fill(0)
pixels.show()
time.sleep(4)

"""
while True:
    for color in COLORS:
        for i in range(NUM_PIXELS):
            #pixels[i] = color
            pixels.fill(0)
            pixels.show()
            time.sleep(DELAY)
"""
            
