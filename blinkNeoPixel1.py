import machine, neopixel
import time

Period = 1.25 #Период мигания светодиода

#Pins
NeoPixelPin = 16
NeoPixelLength = 1
#Colors

Red0 = 255
Green0 = 0
Blue0 = 64

Red1 = 64
Green1 = 0
Blue1 = 255

Color0 = (Red0, Green0, Blue0)
Color1 = (Red1, Green1, Blue1)

# Подпрограммы

def draw(color):
    if color == 0:
        #np[0] = (Red0, Green0, Blue0)
        np[0] = (Color0[0], Color0[1], Color0[2])
    else:
        #np[0] = (Red1, Green1, Blue1)
        np[0] = (Color1[0], Color1[1], Color1[2])
    np.write()
    
#Начальная установка
np = neopixel.NeoPixel(machine.Pin(NeoPixelPin), NeoPixelLength)

#np[0] = (Red0, Green0, Blue0)
#np.write()

#np[0] = (Red1, Green1, Blue1)
#np.write()

print("NeopixelZeroBlink1")

while 1:
    #np[0] = (Red0, Green0, Blue0)
    #np.write()
    draw(0)
    time.sleep(Period / 2)
    #np[0] = (Red1, Green1, Blue1)
    #np.write()
    draw(1)
    time.sleep(Period / 2)
