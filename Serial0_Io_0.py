import machine, neopixel
from machine import UART, Pin
import time

#Pins
NeoPixelPin = 16
NeoPixelLength = 1

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
SendFrameCounter = 0
MessageHead = "Sink from UART0:"

#Global Variables
Command = ""
Parameter = ""

#Main loop
while True:
    if(uart0.any()):
        data = uart0.read()
        if(len(data) > 0):
            Message = MessageHead
            IndexOctoporp = str(data).find('#')
            if(IndexOctoporp >= 0):
                draw(Green)
                sub = str(data)[IndexOctoporp + 1:]
                #IndexColon = str(data).find(':')
                IndexColon = str(sub).find(':')
                IndexCR = str(sub).find('\n')
                if(IndexColon >= 0):
                    Command = sub[0:IndexColon]
                    Parameter = sub[IndexColon + 1:IndexCR - 2]
                else:
                    Command = sub
                    Parameter = ""
            else:
                draw(SkyBlue)
                Command = ""
                Parameter = ""
                    
            Message += str(data)
            Message += " #="
            Message += str(IndexOctoporp)
            if(IndexColon >= 0):
                Message += " :="
                Message += str(IndexColon)
                Message += " CR="
                Message += str(IndexCR)
            Message += " Command="
            Message += Command
            Message += " Parameter="
            Message += Parameter
                
            print(Message)
            uart0.write(data)
        
    
 