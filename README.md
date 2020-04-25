# circuitpython-ledmatrix

The MatrixN class in this CircuitPython module maps an NxM pixel grid onto one or more 8x8 max7219 driven LED displays. It is based on the adafruit max7219 matrix library.

The LED matrices are connected in a single chain in row-first order. I.e., a 16x16 pixel grid would be displayed on 2x2 LED grids. The first two LED grids would be the rows 1 to 8, the next two LED grids would be rows 9 to 16, and so on.

MatrixN has been tested on CircuitPython 5.2.0.

## Use:
This module depends on the modules listed below. To use, copy those modules plus this one to the `lib` directory on your board. Then, use the following:

```python
from ledmatrix import MatrixN
display = MatrixN(spi, cs, width, height)
```
Review the included example script for a complete sample.

## Class:
```python
from ledmatrix import MatrixN
display = MatrixN(spi, cs, width, height)
```
**spi**: a busio object  
**cs**: DigitalInOut pin used for chip select  
**width**: int pixel width of display  
**height**: int pixel height of display  

## Methods:
```python
init_display()
```
Initializes all of the connected LED displays. Must be called before before other commands are issued.

```python
brightness(value)
```

**value**: brightness from 0 to 15  
Sets the brightness of all connected LED displays.

```python
write_cmd(cmd, values)
```

**cmd**: register/commad to apply to each of the values  
**values**: a list of values that will each be paired with cmd and sent out to the displays  

This is used internally by the class for controlling and showing pixels on the display and is not generally required by the developer.

```python
text(strg, xpos, ypos, color=1)
```

Writes a text string into the display frame buffer. Nothing will be displayed until a `show()` command is issued to show the frame buffer on the LED displays

```python
clear_all(color=0)
```

Clears the frame buffer to the specified color. Default is 0 which turns the LEDs off. Odd color values turn LEDs on. Even color values turn the LEDs off.

```python
show()
```

Shows the current frame buffer on the LED displays.