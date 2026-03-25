import machine, neopixel
from machine import Pin
print("NeopixelZero0")
#Pins
NeoPixelPin = 16
NeoPixelLength = 1
#Colors
Red = 255
Green = 0
Blue = 64
np = neopixel.NeoPixel(machine.Pin(NeoPixelPin), NeoPixelLength)
np[0] = (Red, Green, Blue)
np.write()
