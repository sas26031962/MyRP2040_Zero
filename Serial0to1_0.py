'''
Программа для проверки и последовательных портов 
Подключение:
Uart1 -> Txd[D4](RP2040 Zero)
Uart1 -> Rxd[D5](RP2040 Zero)
Uart1 -> Txd[D4](RP2040 Zero)
Uart1 -> Rxd[D5](RP2040 Zero)
LedGreen -> [D6](RP2040 Zero)
LedYellow ->[D7](RP2040 Zero)
'''
import machine, neopixel
from machine import UART, Pin
import time

#Pins
NeoPixelPin = 16
NeoPixelLength = 1

Set = Pin(6, Pin.OUT)
Set.low()

CS  = Pin(7, Pin.OUT)
CS.low()

#===Colors===

Fuxia = (255, 0, 64)
SkyBlue = (64, 0, 255)
Darkness = (0, 0, 0)
Green = (64, 255, 0)

#Subprogramms
def draw(color):
    np[0] = color 
    np.write()

#Setup
np = neopixel.NeoPixel(machine.Pin(NeoPixelPin), NeoPixelLength)
draw(Fuxia)
time.sleep(1)
draw(SkyBlue)
time.sleep(1)
draw(Darkness)

#Ports
uart0 = UART(0, baudrate=115200, tx = Pin(0), rx = Pin(1))
uart1 = UART(1, baudrate=9600, tx = Pin(4), rx = Pin(5))

print("Serial 0 to 1 programm")

#Main loop
while True:
    if uart0.any():
        Set.high()
        data0 = uart0.read()
        uart1.write(data0)
        Message = "Sink from Uart0:"
        Message += str(data0)
        print(Message)
    else:
        Set.low()
        
    if uart1.any():
        CS.high()
        data1 = uart1.read()
        uart0.write(data1)
        Message = "Sink from Uart1:"
        Message += str(data1)
        print(Message)
    else:
        CS.low()
        
    
 