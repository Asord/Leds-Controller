from tkinter import Button, StringVar, Frame, Spinbox, Scale
from tkinter import HORIZONTAL, E, W
from tkinter.colorchooser import askcolor

from LedsInterface.Utilities.Colors import Color

from LedsInterface.base import baseModule

class singleColor_module(baseModule):
    def __init__(self, parent):
        baseModule.__init__(self, parent)

        self._hexColor = "#ffffff"
        self._V3_HSVColor = [0.0, 1.0, 1.0]

        self.mainFrame = Frame(parent)
        self.mainFrame.grid(sticky=(E, W))
        self.populateInterface(self.mainFrame)

    def populateInterface(self, parent):
        """
        populate the parent element with all SingleColor elements
        :param parent: the parent element of all subelements
        """

        """#################### LUMINOSITY ####################"""
        self._SV_luminosity = StringVar(value="100")
        self._S_luminosity = Scale(parent, from_=0, to=100, orient=HORIZONTAL, variable=self._SV_luminosity)
        self._S_luminosity.grid(row=0, column=0, columnspan=2, sticky=(E, W))

        """#################### COEF ####################"""
        self._SV_coefEnabled = StringVar(value="on")

        self._RB_coefs = self._createToggle(parent, "Disable Coef", "Enable Coef", self._SV_coefEnabled)
        self._RB_coefs[0].grid(row=1, column=0)
        self._RB_coefs[1].grid(row=1, column=1)

        """#################### STROBE ####################"""
        self._f_strobeValue = 1.0
        self._d_strobeDirection = -1
        self._SV_strobeEnabled = StringVar(value="off")

        self._RB_strobe = self._createToggle(parent, "Disable Strobe", "Enable Strobe", self._SV_strobeEnabled)
        self._RB_strobe[0].grid(row=2, column=0)
        self._RB_strobe[1].grid(row=2, column=1)

        _SV_strobeSpeed = StringVar(self._parent); _SV_strobeSpeed.set("25")
        self._S_strobeSpeed = Spinbox(parent, from_=2, to=350, textvariable=_SV_strobeSpeed)
        self._S_strobeSpeed.grid(row=3, column=0, columnspan=2, sticky=(E, W))

        """#################### RAINBOW ####################"""
        self._SV_rainbowEnabled = StringVar(value="off")

        self._RB_rainbow = self._createToggle(parent, "Disable Rainbow", "Enable Rainbow", self._SV_rainbowEnabled)
        self._RB_rainbow[0].grid(row=4, column=0)
        self._RB_rainbow[1].grid(row=4, column=1)

        _SV_rainbowSpeed = StringVar(self._parent); _SV_rainbowSpeed.set("6")
        self._S_rainbowSpeed = Spinbox(parent, from_=1, to=3600, textvariable=_SV_rainbowSpeed)
        self._S_rainbowSpeed.grid(row=5, column=0, columnspan=2, sticky=(E, W))


        """#################### COLOR PICKER ####################"""
        self._B_pickColor = Button(parent, command=self._pickColor, width=21, height=5)
        self._B_pickColor.configure(background=self._hexColor)
        self._B_pickColor.grid(row=6, column=0, columnspan=2)

    def _switchRainbow(self):
        if self._SV_rainbowEnabled.get() == "on":
            self._V3_HSVColor = [0.0, 1.0, 1.0]
        else:
            self._V3_HSVColor = [0.0, 0.0, 1.0]

    def _switchFlash(self):
        if self._SV_strobeEnabled.get() == "off":
            self._f_strobeValue = 1.0
            self._d_strobeDirection = -1

    def __updateRainbow(self):
        _rainbowValue = self._safeGetValueFromSlider(self._S_rainbowSpeed, 10, 0.6)

        self._V3_HSVColor[0] = (self._V3_HSVColor[0] + _rainbowValue) % 360
        RGB = Color.fromHSV(*self._V3_HSVColor)
        self._hexColor = RGB.toHex()

    def __updateStrobe(self):
        _strobeValue = self._safeGetValueFromSlider(self._S_strobeSpeed, 1000, 0.025)

        self._f_strobeValue = self._f_strobeValue + _strobeValue * self._d_strobeDirection
        if (1 - _strobeValue < self._f_strobeValue) or (self._f_strobeValue < _strobeValue):
            self._d_strobeDirection *= -1

    def _pickColor(self):
        if self._SV_rainbowEnabled.get() == "off":
            self._hexColor = askcolor()[1]

    def update(self):
        """ Update the leds from interface parametters """

        """ Computer color if rainbow is enabled """
        if self._SV_rainbowEnabled.get() == "on":
            self.__updateRainbow()

        """ Computer value if strobe is enabled """
        if self._SV_strobeEnabled.get() == "on":
            self.__updateStrobe()

        """ Update color value with strobeValue """
        _Color_RGB = Color.fromHex(self._hexColor)
        _Color_RGB *= self._f_strobeValue

        """ Update button color """
        self._B_pickColor.configure(background=_Color_RGB.toHex())

        """ Computer color luminosity from slider """
        _Color_RGB *= int(self._S_luminosity.get()) / 100

        """ Computer color coefs """
        if self._SV_coefEnabled.get() == "on":
            _rgbList = _Color_RGB.mul([1.0, 0.42, 0.3]).toList()
        else:
            _rgbList = _Color_RGB.toList()

        """ Send colors to arduino and wait 60ms """
        for n in range(self._controller.nbLeds): self._controller.buffer[n] = _rgbList
        self._controller.send()
