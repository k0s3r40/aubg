from time import sleep
from stripcontroller import StripController

s = StripController()

s.G()
sleep(1)
s.BG()
sleep(1)
s.Y()
sleep(1)
s.R()
sleep(1)

print("OK")

