import time, _thread, machine
from machine import Pin

def task(n, delay):
    LedPin = 25  
    led = Pin(LedPin, Pin.OUT)
    for i in range(n):
        led.high()
        time.sleep(delay)
        led.low()
        time.sleep(delay)
    print('>done')
 
print("Multicore example: \n >start") 
_thread.start_new_thread(task, (20, 0.5))
