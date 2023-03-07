import time

import matplotlib.pyplot as draw


def drawing(x_value, y_value):
    draw.ion()
    draw.grid()
    draw.xlabel('f [MHz]')
    draw.ylabel('U [dBuV]')
    draw.xscale('log')
    draw.plot(x_value, y_value)
    time.sleep(1)


while True:
    print("Podaj x: ")
    x = int(input())
    print("Podaj y: ")
    y = int(input())
    drawing(x, y)
