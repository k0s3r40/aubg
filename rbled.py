import time
from gpiozero import LED
green = LED(18)
green.on()


red = LED(15)

blue = LED(14)


green.off()
time.sleep(3)
green.on()
red.off()
time.sleep(3)
red.on()
blue.off()
time.sleep(3)
blue.on()


