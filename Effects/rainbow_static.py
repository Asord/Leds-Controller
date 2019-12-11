from LedsInterface.Utilities.ArduinoController import *

from LedsInterface.Utilities.Colors import Color
from time import sleep

def __effect_rainbowstatic_semi(cls, colorRange, steps):
    cls.clear()

    if cls.vars["rainbowClockwise"]:
        if cls.vars["rainbowHue"] >= colorRange[1]:
            cls.vars["rainbowClockwise"] = not cls.vars["rainbowClockwise"]
    else:
        if cls.vars["rainbowHue"] <= colorRange[0]:
            cls.vars["rainbowClockwise"] = not cls.vars["rainbowClockwise"]

    color = Color.fromHSV(cls.vars["rainbowHue"], 1.0, 1.0)

    for c in range(cls.nbLeds):
        cls.buffer[c] = color.toList()

    if cls.vars["rainbowClockwise"]:
        cls.vars["rainbowHue"] = (cls.vars["rainbowHue"] + steps) % 360
    else:
        cls.vars["rainbowHue"] = (cls.vars["rainbowHue"] - steps) % 360

    cls.send()

def __effect_rainbowstatic_full(cls, steps):
    cls.clear()

    color = Color.fromHSV(cls.vars["rainbowHue"], 1.0, 1.0)

    for c in range(cls.nbLeds): cls.buffer[c] = color.toList()

    cls.vars["rainbowHue"] = (cls.vars["rainbowHue"] + steps) % 360

    cls.moderate(1, 0.3, 0.42)
    cls.send()

def rainbow_static(controller, colorRange=(0.0, 360.0), steps=1.0):

    controller.vars.clear()
    controller.vars["rainbowHue"] = colorRange[0]

    if colorRange[1] < 360:
        controller.vars["rainbowClockwise"] = True
        return __effect_rainbowstatic_semi, (controller, colorRange, steps)
    else:
        return __effect_rainbowstatic_full, (controller, steps)


if __name__ == '__main__':
    arduino = ArduinoController()
    func, param = rainbow_static(arduino, steps=0.05)

    while True:
        func(*param)
        sleep(0.05)