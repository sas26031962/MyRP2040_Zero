import time, _thread, machine
import utime
from machine import Pin

#Task for core 1
def task(n, delay):
    LedPin = 25  
    led = Pin(LedPin, Pin.OUT)
    Task1Counter = 0
    
    for i in range(n):
        Task1Counter = Task1Counter + 1
        print("Core1: Task1Counter=" + str(Task1Counter))
        #count = count + 1
        #print("Core1: Task1Counter=" + str(count)) 
        led.high()
        time.sleep(delay)
        led.low()
        time.sleep(delay)
    print('\n>Core1 task done\n')
 
print("Core1 task start")

Task1Counter = 0;

_thread.start_new_thread(task, (20, 0.5))

#Task for core 2
Task2Counter = 0
sensor_temp = machine.ADC(4) #Connect to internal temperature sensor
conversion_factor = 3.3 / (65535)

print("Core2 task start") 

while True:
    Task2Counter = Task2Counter + 1
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706)/0.001721
    if (Task1Counter < 19):
        print("Core2: Task2Counter=" + str(Task2Counter) + " temperature=" + str(temperature) + " | Task1Counter=" + str(Task1Counter))
    utime.sleep(2)


