import time
import busio
import digitalio
from board import TX, RX, A1

from multimatrix import MultiMatrix

WIDTH = const(32)
HEIGHT = const(8)

mosi = TX
clk = RX
cs = digitalio.DigitalInOut(A1)
spi = busio.SPI(clk, MOSI=mosi)

display = MultiMatrix (spi, cs, WIDTH, HEIGHT, orientation=0)

# Fill columns right, left
def wipe_pixels_vertical():
    display.fill(0)
    for x in range(WIDTH):
        for y in range(HEIGHT):
            display.pixel(x, y, 1)
        display.show()
    for x in range(WIDTH-1, -1, -1):
        for y in range(HEIGHT-1, -1, -1):
            display.pixel(x, y, 0)
        display.show()

# Fill rows down, up
def wipe_pixels_horizontal():
    display.fill(0)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            display.pixel(x, y, 1)
        display.show()
    for y in range(HEIGHT-1, -1, -1):
        for x in range(WIDTH-1, -1, -1):
            display.pixel(x, y, 0)
        display.show()

def scan_right():
    # one column of leds lit
    for c in range(WIDTH):
        display.pixel(0, c, 1)
    display.show()

    # now scroll the column to the right
    for j in range(WIDTH):
        display.scroll(1, 0)
        display.show()
    pause()

def text():
    # scroll a string across the display
    s = "blink!"
    for pixel_position in range(WIDTH, -(len(s) * 6)-1, -1):
        display.fill(0)
        display.text(s, pixel_position, 0)
        display.show()
        pause(0.1)


def pause(percent=1):
    time.sleep(0.4 * percent)

while True:

    # all lit up
    display.clear_all(1)
    display.show()
    pause(2)

    # all off
    display.clear_all()
    display.show()
    pause()

    wipe_pixels_vertical()
    pause()

    wipe_pixels_horizontal()
    pause()

    text()

