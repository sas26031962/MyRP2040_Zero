import machine, neopixel
from machine import Pin
print("Neopixel0")
#Colors
Red = 255
Green = 128
Blue = 64
np = neopixel.NeoPixel(machine.Pin(16), 1)
np[0] = (Red,0,0)
np[1] = (0,Green,0)
np[2] = (0,0,Blue)
