import machine, neopixel
import time
import asyncio

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

PERIOD = 400

#=========================================================    
# Подпрограммы
#=========================================================
def draw(color):
    if color == 0:
        #np[0] = (Red0, Green0, Blue0)
        np[0] = (Color0[0], Color0[1], Color0[2])
    else:
        #np[0] = (Red1, Green1, Blue1)
        np[0] = (Color1[0], Color1[1], Color1[2])
    np.write()
    
async def blinkAS(period_ms):
    while True:
        draw(0)
        await asyncio.sleep_ms(period_ms)
        draw(1)
        await asyncio.sleep_ms(period_ms)
        
async def main():
    asyncio.create_task(blinkAS(PERIOD))
    await asyncio.sleep_ms(10_000)
    
#=========================================================    

#=========================================================    
#Начальная установка
#=========================================================    
np = neopixel.NeoPixel(machine.Pin(NeoPixelPin), NeoPixelLength)

print ("===blinkNeoPixelAsync1=>Begin")
asyncio.run(main())
print ("===blinkNeoPixelAsync1=>End")
