import os
import time
import datetime

while True:
    os.system('clear')
    t = time.asctime()
    h = datetime.datetime.now()
    print(t)
    print(h)
    time.sleep(1)