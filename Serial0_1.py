from machine import UART, Pin
import time

uart0 = UART(0, baudrate=115200, tx = Pin(0), rx = Pin(1))
SendFrameCounter = 0
MessageHead = "Send from UART0:"

while True:
    Message = MessageHead
    Message += str(SendFrameCounter)
    Message += "\n\r"
    #uart0.write("Hello from UART0!\n\r")
    uart0.write(Message)
    print("Print Message to UART0")
    
    SendFrameCounter = SendFrameCounter + 1
    time.sleep(1)