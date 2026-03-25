from machine import UART, Pin
import time

uart1 = UART(1, baudrate=115200, tx = Pin(4), rx = Pin(5))
SendFrameCounter = 0
SinkFrameCounter = 0
#MessageHead = "Send to UART1:"
MessageHead = "Sink from UART1:"

while True:
    if uart1.any():
        Data = uart1.read()
        #Message = MessageHead
        #Message += Data
        #print(Message)
        print('Resived', Data)
        #SinkFrameCounter = SinkFrameCounter + 1
    
    #Message = MessageHead
    #Message += str(SendFrameCounter)
    #Message += "\n\r"
        uart1.write(Data)
    #print("Print Message to UART1")
    
    #SendFrameCounter = SendFrameCounter + 1
    #time.sleep(1)
    #===================================