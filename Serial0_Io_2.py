'''
Программа для проверки и управления модулем JDY-41
Подключение:
Rxd(JDY-41) -> Txd[D4](RP2040 Zero)
Txd(JDY-41) -> Rxd[D5](RP2040 Zero)
Set(JDY-41) ->    [D6](RP2040 Zero)
Cs (JDY-41) ->    [D7](RP2040 Zero)
'''
import machine, neopixel
from machine import UART, Pin
import time

#Pins
NeoPixelPin = 16
NeoPixelLength = 1

Set = Pin(6, Pin.OUT)
Set.high()

CS  = Pin(7, Pin.OUT)
CS.high()

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

CS.low()

#Ports
uart0 = UART(0, baudrate=115200, tx = Pin(0), rx = Pin(1))
uart1 = UART(1, baudrate=9600, tx = Pin(4), rx = Pin(5))

SendFrameCounter = 0
MessageHead = "Sink from UART0:"

#Global Variables
Command = ""
Parameter = ""

print("Incoming from Uart0, Sink from Uart1 and sent to Uart0")

#Main loop
while True:
    #=== Приём из порта 0
    if(uart0.any()):
        data = uart0.read()
        if(len(data) > 0):
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
                    Command = sub[0:IndexCR - 2]
                    Parameter = ""
            else:
                Command = ""
                Parameter = ""
            #---Формирование ответного сообщения            
            Message = MessageHead
            Message += str(data)
            Message += " Command="
            Message += Command
            Message += " Parameter="
            Message += Parameter
            #---Разбор команды
            if Command == "Cs":
                Message += " Cs="
                if Parameter == "0":
                    CS.low()
                    Message += "0"
                    uart0.write("Cs=0\n")
                else:
                    CS.high()
                    Message += "1"
                    uart0.write("Cs=1\n")
            #---        
            if Command == "Set":
                Message += " Set="
                if Parameter == "0":
                    Set.low()
                    Message += "0"
                    uart0.write("Set=0\n")
                else:
                    Set.high()
                    Message += "1"
                    uart0.write("Set=1\n")
            #---
            if Command == "Reset":
                Message += " > Reset: 0xAB, 0xE3, 0x0D, 0x0A"
                SendingData1 = bytearray([0xAB, 0xE3, 0x0D, 0x0A])
                uart1.write(SendingData1)
                SendingData0 = bytearray([0x52, 0x65, 0x73, 0x65, 0x74, 0x0D, 0x0A]) # Reset\n\r
                uart0.write(SendingData0)
            #---
            if Command == "ConfigId":
                Message += " > ConfigId: 0xA9, 0xE1, 0x04, 0x00, 0x09, 0xA0, 0x66, 0x77, 0x88, 0x55, 0x01, 0x00, 0x0D, 0x0A"
                SendingData1 = bytearray([0xA9, 0xE1, 0x04, 0x00, 0x09, 0xA0, 0x66, 0x77, 0x88, 0x55, 0x01, 0x00, 0x0D, 0x0A])
                uart1.write(SendingData1)
                SendingData0 = Command
                SendingData0 += '\n'
                SendingData0 += '\r'
                uart0.write(SendingData0)
            #---
            if Command == "ConfigRole":
                Message += " > ConfigRole: 0xA9, 0xE3, 0xA0, 0x0D, 0x0A"
                SendingData1 = bytearray([0xA9, 0xE3, 0xA0, 0x0D, 0x0A])
                uart1.write(SendingData1)
                SendingData0 = Command
                SendingData0 += '\n'
                SendingData0 += '\r'
                uart0.write(SendingData0)
            #---
            if Command == "Send":
                Message += " > Send:"
                Message += Parameter
                SendingData1 = Parameter
                #SendingData1 = bytearray([0x30, 0x31, 0x32, 0x0D, 0x0A])
                uart1.write(SendingData1)
                SendingData0 = Command
                SendingData0 += ':'
                SendingData0 += Parameter
                SendingData0 += '\n'
                SendingData0 += '\r'
                uart0.write(SendingData0)
            #---

                
            print(Message)
            #uart0.write(data)
            #---
            draw(Darkness)
            
    #===Приём из порта 1    
    if uart1.any():
        draw(SkyBlue)
        data1 = uart1.read()
        #uart0.write(data1)
        Message = "Sink from Uart1:"
        Message += str(data1)
        print(Message)
        #---
        draw(Darkness)
    
 