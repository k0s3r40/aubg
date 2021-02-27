import time
from gpiozero import LED

class StripController():
    def __init__(self, green_addr = 18, red_addr=15, blue_addr=14):
        self.green = LED(green_addr)
        self.green.on() # means off and vice versa
        self.red = LED(red_addr)
        self.red.on()
        self.blue = LED(blue_addr)
        self.blue.on()
    

    def reset(self):
        self.green.on()
        self.red.on()
        self.blue.on()
        
    
    def G(self):
        self.reset()
        self.green.off()

    def R(self):
        self.reset()
        self.red.off()

    def B(self):
        self.reset()
        self.blue.off()


