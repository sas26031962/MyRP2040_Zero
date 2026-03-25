import time
from machine import I2C
from machine import Pin

#sdaPIN = machine.Pin(0)
#sclPIN = machine.Pin(1)
sdaPIN = machine.Pin(12)
sclPIN = machine.Pin(13)

i2c = machine.I2C(0, sda=sdaPIN, scl=sclPIN, freq= 400000)
print('Scanning I2C bus...')
devices = i2c.scan()
if(len(devices) == 0):
    print("No i2c device!")
else:
    print('i2c devices found:',len(devices))
    for device in devices:
        print("Decimal address: ", device, " | Hex address: ",hex(device))

Period = 0.5 #Период мигания светодиода
LedPin = 25  #Вывод управления встроенным светодиодом

led = Pin(LedPin, Pin.OUT)

while 1:
    led.low()
    time.sleep(Period / 2)
    led.high()
    time.sleep(Period / 2)
