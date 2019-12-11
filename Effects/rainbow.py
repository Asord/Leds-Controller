from LedsInterface.Utilities.ArduinoController import *

from LedsInterface.Utilities.Colors import Color
from time import sleep

def __effect_rainbow(cls, steps):
    cls.clear()

    hue = cls.vars["startHue"]

    for c in range(cls.nbLeds):
        hue = (hue + steps) % 360
        col = Color.fromHSV(hue, 1.0, 1.0)
        cls.buffer[c] = col.toListLED()

    cls.vars["startHue"] = (cls.vars["startHue"] - steps) % 360

    cls.moderate(1, 0.3, 0.42)
    cls.send()

def rainbow(controller, steps=1.0):
    controller.vars.clear()
    controller.vars["startHue"] = 0

    return __effect_rainbow, (controller, steps)


if __name__ == '__main__':
    arduino = ArduinoController()
    func, param = rainbow(arduino, 6)

    while True:
        func(*param)
        sleep(0.05)