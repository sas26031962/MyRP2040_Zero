from machine import UART, Pin
import time

uart0 = UART(0, baudrate=115200, tx = Pin(0), rx = Pin(1))

while True:
    uart0.write("Hello from UART0!\n\r")
    print("Print'Send to UART0'")
    
    time.sleep(1)