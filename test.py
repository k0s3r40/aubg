from time import sleep
from stripcontroller import StripController

s = StripController()

s.R()
sleep(1)
s.G()
sleep(1)
s.B()
sleep(1)

print("OK")

