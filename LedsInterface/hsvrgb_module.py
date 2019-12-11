from tkinter import StringVar, Frame, Scale
from tkinter import HORIZONTAL, E, W

from LedsInterface.Utilities.Colors import Color
from LedsInterface.base import baseModule

class hsvrgb_module(baseModule):
    def __init__(self, parent):
        baseModule.__init__(self, parent)

        self._color = Color()

        self.mainFrame = Frame(parent)
        self.mainFrame.grid(sticky=(E, W))
        self.populateInterface(self.mainFrame)

    def populateInterface(self, parent):
        """
        populate the parent element with all SingleColor elements
        :param parent: the parent element of all subelements
        """

        """#################### HUE ####################"""
        self._SV_hue = StringVar(value="0")
        self._S_hue  = Scale(parent, from_=0, to=360, orient=HORIZONTAL, variable=self._SV_hue, command=self._change_HSV)
        self._S_hue.grid(row=0, column=0, columnspan=2, sticky=(E, W))
        """#################### SATURATION ####################"""
        self._SV_saturation = StringVar(value="100")
        self._S_saturation = Scale(parent, from_=0, to=100, orient=HORIZONTAL, variable=self._SV_saturation, command=self._change_HSV)
        self._S_saturation.grid(row=1, column=0, columnspan=2, sticky=(E, W))
        """#################### LUMINOSITY ####################"""
        self._SV_value = StringVar(value="100")
        self._S_value = Scale(parent, from_=0, to=100, orient=HORIZONTAL, variable=self._SV_value, command=self._change_HSV)
        self._S_value.grid(row=2, column=0, columnspan=2, sticky=(E, W))


        """#################### RED ####################"""
        self._SV_red = StringVar(value="255")
        self._S_red = Scale(parent, from_=0, to=255, orient=HORIZONTAL, variable=self._SV_red, command=self._change_RGB)
        self._S_red.grid(row=3, column=0, columnspan=2, sticky=(E, W))
        """#################### GREEN ####################"""
        self._SV_green = StringVar(value="0")
        self._S_green = Scale(parent, from_=0, to=255, orient=HORIZONTAL, variable=self._SV_green, command=self._change_RGB)
        self._S_green.grid(row=4, column=0, columnspan=2, sticky=(E, W))
        """#################### BLUE ####################"""
        self._SV_blue = StringVar(value="0")
        self._S_blue = Scale(parent, from_=0, to=255, orient=HORIZONTAL, variable=self._SV_blue, command=self._change_RGB)
        self._S_blue.grid(row=5, column=0, columnspan=2, sticky=(E, W))

    def _getHSVTuple(self):
        return float(self._SV_hue.get()), float(self._SV_saturation.get())/100.0, float(self._SV_value.get())/100.0

    def _getRGBTuple(self):
        return

    def _change_HSV(self, e=None):
        self._color = Color.fromHSV(
            float(self._SV_hue.get()),
            float(self._SV_saturation.get())/100.0,
            float(self._SV_value.get())/100.0)

        self._SV_red.set(self._color.red())
        self._SV_green.set(self._color.green())
        self._SV_blue.set(self._color.blue())

    def _change_RGB(self, e=None):
        self._color = Color(
            int(self._SV_red.get()),
            int(self._SV_green.get()),
            int(self._SV_blue.get()))

        h, s, v = self._color.toHSV()
        self._SV_hue.set(h)
        self._SV_saturation.set(s * 100)
        self._SV_value.set(v * 100)

    def update(self):
        """ Update the leds from interface parametters """
        self._color.toHex()

        """ Update color """
        self.mainFrame.configure(background=self._color.toHex())

        """ Send colors to arduino and wait 60ms """
        for n in range(self._controller.nbLeds): self._controller.buffer[n] = self._color.toList()
        self._controller.send()
