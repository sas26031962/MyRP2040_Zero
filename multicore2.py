from rp2 import PIO
import time, _thread, machine
import utime
from machine import Pin

#Task for core 1
def task1(n, delay):
    LedPin = 25  
    led = Pin(LedPin, Pin.OUT)
    TaskCounter = 0
    
    for i in range(n):
        TaskCounter = TaskCounter + 1
        print("Core1: TaskCounter=" + str(TaskCounter))
        led.high()
        time.sleep(delay)
        led.low()
        time.sleep(delay)
    print('\n>Core1 task done\n')
 
#Task for core 2
def task2(n, delay):
    TaskCounter = 0
    
    for i in range(n):
        TaskCounter = TaskCounter + 1
        print("Core2: TaskCounter=" + str(TaskCounter))
        time.sleep(delay)
    print('\n>Core2 task done\n')
 
print("Core1 task start")

#Start tasks
_thread.start_new_thread(task1, (20, 0.5))

task2(20, 0.5)


