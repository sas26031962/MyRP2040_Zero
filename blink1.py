import time
from machine import I2C
from machine import Pin

Period = 0.25 #Период мигания светодиода
LedPin = 25  #Вывод управления встроенным светодиодом
#LedPin = 16  #Вывод управления встроенным светодиодом

led = Pin(LedPin, Pin.OUT)

print("Hello, Pico Zero!")

while 1:
    led.low()
    time.sleep(Period / 2)
    led.high()
    time.sleep(Period / 2)
