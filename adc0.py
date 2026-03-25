import machine
import utime
from machine import Pin

LedPin = 25  #Вывод управления встроенным светодиодом
led = Pin(LedPin, Pin.OUT)
led.high()

print("Test temperature sensor by ADC program")

sensor_temp = machine.ADC(4) #Connect to internal temperature sensor
conversion_factor = 3.3 / (65535)

while True:
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706)/0.001721
    print(temperature)
    utime.sleep(2)
    

