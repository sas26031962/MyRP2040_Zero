from machine import Pin
from machine import Timer

Period = 1.25 #Период мигания светодиода
LedPin = 25  #Вывод управления встроенным светодиодом

led = Pin(LedPin, Pin.OUT)
tim = Timer()

def tick(timer):
    global led
    led.toggle()

print("Timer test program")

tim.init(freq=3.5, mode=Timer.PERIODIC, callback=tick)
