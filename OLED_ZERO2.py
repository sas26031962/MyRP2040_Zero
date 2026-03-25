from machine import Pin, I2C
#from ssd1306 import SSD1306_I2C
import utime
import framebuf,sys

#==================================================================
# register definitions
SET_CONTRAST = const(0x81)
SET_ENTIRE_ON = const(0xA4)
SET_NORM_INV = const(0xA6)
SET_DISP = const(0xAE)
SET_MEM_ADDR = const(0x20)
SET_COL_ADDR = const(0x21)
SET_PAGE_ADDR = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP = const(0xA0)
SET_MUX_RATIO = const(0xA8)
SET_COM_OUT_DIR = const(0xC0)
SET_DISP_OFFSET = const(0xD3)
SET_COM_PIN_CFG = const(0xDA)
SET_DISP_CLK_DIV = const(0xD5)
SET_PRECHARGE = const(0xD9)
SET_VCOM_DESEL = const(0xDB)
SET_CHARGE_PUMP = const(0x8D)

# Subclassing FrameBuffer provides support for graphics primitives
# http://docs.micropython.org/en/latest/pyboard/library/framebuf.html
class SSD1306(framebuf.FrameBuffer):
    def __init__(self, width, height, external_vcc):
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.init_display()

    def init_display(self):
        for cmd in (
            SET_DISP | 0x00,  # off
            # address setting
            SET_MEM_ADDR,
            0x00,  # horizontal
            # resolution and layout
            SET_DISP_START_LINE | 0x00,
            SET_SEG_REMAP | 0x01,  # column addr 127 mapped to SEG0
            SET_MUX_RATIO,
            self.height - 1,
            SET_COM_OUT_DIR | 0x08,  # scan from COM[N] to COM0
            SET_DISP_OFFSET,
            0x00,
            SET_COM_PIN_CFG,
            0x02 if self.width > 2 * self.height else 0x12,
            # timing and driving scheme
            SET_DISP_CLK_DIV,
            0x80,
            SET_PRECHARGE,
            0x22 if self.external_vcc else 0xF1,
            SET_VCOM_DESEL,
            0x30,  # 0.83*Vcc
            # display
            SET_CONTRAST,
            0xFF,  # maximum
            SET_ENTIRE_ON,  # output follows RAM contents
            SET_NORM_INV,  # not inverted
            # charge pump
            SET_CHARGE_PUMP,
            0x10 if self.external_vcc else 0x14,
            SET_DISP | 0x01,
        ):  # on
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def poweroff(self):
        self.write_cmd(SET_DISP | 0x00)

    def poweron(self):
        self.write_cmd(SET_DISP | 0x01)

    def contrast(self, contrast):
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(SET_NORM_INV | (invert & 1))

    def show(self):
        x0 = 0
        x1 = self.width - 1
        if self.width == 64:
            # displays with width of 64 pixels are shifted by 32
            x0 += 32
            x1 += 32
        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(x0)
        self.write_cmd(x1)
        self.write_cmd(SET_PAGE_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        self.write_data(self.buffer)


class SSD1306_I2C(SSD1306):
    def __init__(self, width, height, i2c, addr=0x3C, external_vcc=False):
        self.i2c = i2c
        self.addr = addr
        self.temp = bytearray(2)
        self.write_list = [b"\x40", None]  # Co=0, D/C#=1
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.temp[0] = 0x80  # Co=1, D/C#=0
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_data(self, buf):
        self.write_list[1] = buf
        self.i2c.writevto(self.addr, self.write_list)

#==================================================================

WIDTH  = 128                                           # oled display width
HEIGHT = 64                                            # oled display height

image_byte_arr = b'BM\xbe\x00\x00\x00\x00\x00\x00\x00>\x00\x00\x00(\x00\x00\x00 \x00\x00\x00 \x00\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x80\x00\x00\x00\xc4\x0e\x00\x00\xc4\x0e\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xfc?\xff\xff\xfb\xcf\xff\xff\xe7\xf7\xff\xff\xc7\xf1\xff\xffs\xc6\x7f\xfe\xf1\xcf\xbf\xfd\xf7\xef\xbf\xfd\xf7\xf7\xdf\xff\xff\xf7\xdf\xfb\xef\xf3\xdf\xf9\xc7\xf1\x8f\xf6\x13\xeco\xf7|>w\xf7~\x7fw\xf7\xfe\x7fw\xf7\xff\x7fo\xfb\x7f\x7fo\xfc~~\x1f\xfd\xbc=\xff\xff\xe3\xe3\xbf\xfe\xf7\xf7\xbf\xff\x7f\xff\x7f\xff3\xe4\xff\xffx\x1f\x7f\xfe\xfc?\xbf\xfd\xfe?\xff\xfb\xff\x7f\xdf\xfb\xff\x7f\xdf\xfb\xfe\x7f\xef\xfb\xff\xbf\xef\xf9\xfb\xdf\x9f\xff\x0f\xf0\xff'
image_width = 32
image_height = 32

#OLED I2C Configuration
#sdaPIN = machine.Pin(0)
#sclPIN = machine.Pin(1)
sdaPIN = machine.Pin(12)
sclPIN = machine.Pin(13)

i2c = machine.I2C(0, sda=sdaPIN, scl=sclPIN, freq= 200000)

print("I2C Address      : " + hex(i2c.scan()[0]).upper()) # Display device address
print("I2C Configuration: " + str(i2c))                   # Display I2C config
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c) # Init oled display



#OLED Text display Function
def displayText(text, position=(0,0),clear_oled=True,show_text=True):
    if clear_oled:
        oled.fill(0) # Clear the oled display in case it has junk on it.
    oled.text(text,position[0],position[1]) # dispaying text
    if show_text:
        oled.show()  # Updating the display
        
        
#OLED Image display function
        
def displayImage(image_byte_array, image_resolution,position=(0,0),clear_oled=False,show_img=True):
    img = bytearray(image_byte_array)
    img = bytearray([img[i] for i in range(len(img)-1,-1,-1)])
    
    frame = framebuf.FrameBuffer(img, image_resolution[0], image_resolution[1], framebuf.MONO_HMSB) # MONO_HLSB, MONO_VLSB, MONO_HMSB
    
    if clear_oled:
        oled.fill(0) # clear the OLED
        print("clear")
    if show_img:
        oled.blit(frame, position[0],position[1]) # show the image at location (x=0,y=0)
        oled.show()
        
        print("display")

#==================================================================

#Display Text on OLED
digits = "1234567890"
text1 = "Digit:"
text2 = "Line 2:"
text3 = "Line 3:"

displayText(text1 + digits,(0,0),clear_oled=False,show_text=True)
displayImage(image_byte_arr,(image_width,image_height),(0,8),clear_oled=False)

