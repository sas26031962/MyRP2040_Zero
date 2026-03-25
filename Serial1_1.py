from machine import UART, Pin
import time

uart1 = UART(1, baudrate=115200, tx = Pin(4), rx = Pin(5))
SendFrameCounter = 0
MessageHead = "Send from UART1:"

while True:
    Message = MessageHead
    Message += str(SendFrameCounter)
    Message += "\n\r"
    uart1.write(Message)
    print("Print Message to UART1")
    
    SendFrameCounter = SendFrameCounter + 1
    time.sleep(1)