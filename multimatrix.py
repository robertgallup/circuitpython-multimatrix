from adafruit_max7219 import max7219
import math

class MultiMatrix(max7219.MAX7219):
    """
    Driver for LED matrices based on the MAX7219 chip.
    Supports multi-matrix displays.
    Automatically calculates number of 8x8 modules based on grid size

    :param object spi: an spi busio or spi bitbangio object
    :param ~digitalio.DigitalInOut cs: digital in/out to use as chip select signal
    :param int width: pixel width of grid (default=8)
    :param int height: pixel height of grid (default=8)
    """

    # Register definitions
    _DECODEMODE     = const(0b1001) #  9
    _SCANLIMIT      = const(0b1011) # 11
    _SHUTDOWN       = const(0b1100) # 12
    _DISPLAYTEST    = const(0b1111) # 15
    _DIGIT0         = const(0b0001) #  1
    _INTENSITY      = const(0b1010) # 10

    def __init__(self, spi, cs, width=8, height=8, orientation=0):
        # Number of 8x8 LED displays required is calculated as width/8 * height/8
        # ceil() is used to round both up to next whole matrix
        self._num_displays = math.ceil(width/8) * math.ceil(height/8)
        # Display matrix orientation
        self._orienation = orientation

        super().__init__(width, height, spi, cs)

    def init_display(self):
        """
        Initializes displays
        """
        # Initialize important registers
        for cmd, data in (
            (_SHUTDOWN, 0),
            (_DISPLAYTEST, 0),
            (_SCANLIMIT, 7),
            (_DECODEMODE, 0),
            (_SHUTDOWN, 1),
        ):
            self.write_cmd(cmd, [data] * self._num_displays)

    def brightness(self, value):
        """
        Sets the brightness of all displays.

        :param int value: 0->15 dimmest to brightest
        """
        self.write_cmd(_INTENSITY, [value&0xFF] * self._num_displays)

    def write_cmd(self, cmd, values):
        """
        Writes a list of values using the same register command
        before each value

        :param int cmd: a single command (e.g. register number)
        :param list values: a list of values.
        """
        # Command list of alternating cmd and value pairs
        # cmd_list = [[cmd, v] for v in values]
        cmd_list = []
        for v in values: cmd_list += [cmd, v]
        # Set CS low and write the command list to the devices
        self._chip_select.value = 0
        with self._spi_device as spi:
            spi.write(bytearray(cmd_list))

    def text(self, strg, xpos, ypos, color=1):
        """
        Write text into frame buffer for LED matrix

        :param int xpos: x position
        :param int ypos: y position
        :param string strg: string to place in buffr
        :param color: Odd number sets the text, clears otherwise
        """
        self.framebuf.text(strg, xpos, ypos, color & 0x01)

    def clear_all(self, color=0):
        """
        Clears display. Default is clear to 0.

        :param int color: even is clear to LED off, odd is LED on
        """
        self.fill(color & 0X01)

    def show(self):
        """
        Updates all displays from the frame buffer
        """
        # Each matrix takes 8 bytes (one per row). So, the same rows on
        # different matrices are 8 bytes apart in the frame buffer. But,
        # the rows must be output in reverse matrix order, i.e. data for
        # the last matrix in the chain is output first (just like a shift
        # register), then the next closest one, and so on.
        v = 0
        values = bytearray(self._num_displays)
        for y in range(8):

            if self._orienation == 1:

                d = self._num_displays
                for display in range(self._num_displays):
                    d -= 1
                    for x in range(8):
                        v = (v >> 1) | ((self._buffer[(d * 8) + x] << y) & 0b10000000)
                    values[display] = v

            else:
                d = self._num_displays
                for display in range(self._num_displays):
                    d -= 1
                    values[display] = self._buffer[y + (d * 8)]

            self.write_cmd(_DIGIT0 + y, values)


