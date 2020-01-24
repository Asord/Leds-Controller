from tkinter import StringVar, Frame, Scale, Button, LabelFrame
from tkinter import HORIZONTAL, E, W

from random import uniform as randrange
from LedsInterface.Utilities.Colors import Color
from LedsInterface.base import baseModule


class shades_module(baseModule):
    def __init__(self, parent):
        baseModule.__init__(self, parent)

        self._color = Color(255, 0, 0)

        self._colors = [Color() for _ in range(10)]

        self.mainFrame = Frame(parent)
        self.mainFrame.grid(sticky=(E, W))

        self.mainFrame.configure(background=self._color.toHex())

        self.populateInterface(self.mainFrame)
        
        self.iupdateCounter = 0
        self.newColors = []

    def populateInterface(self, parent):
        """
        populate the parent element with all SingleColor elements
        :param parent: the parent element of all subelements
        """

        """#################### HUE ####################"""
        self._LF_hue = LabelFrame(parent, text="H")
        self._LF_hue.grid(row=0, column=0, sticky=(E, W))

        self._SV_hue = StringVar(value="0")
        self._S_hue = Scale(self._LF_hue, from_=0, to=360, orient=HORIZONTAL, variable=self._SV_hue, command=self._change_HSV)
        self._S_hue.grid(row=0, column=0, columnspan=2, sticky=E)

        self._SV_hueD = StringVar(value="60")
        self._S_hueD = Scale(self._LF_hue, from_=0, to=120, orient=HORIZONTAL, variable=self._SV_hueD)
        self._S_hueD.grid(row=1, column=0, columnspan=2, sticky=E)

        """#################### SATURATION ####################"""
        self._LF_saturation = LabelFrame(parent, text="S")
        self._LF_saturation.grid(row=1, column=0, sticky=(E, W))

        self._SV_saturation = StringVar(value="100")
        self._S_saturation = Scale(self._LF_saturation, from_=0, to=100, orient=HORIZONTAL, variable=self._SV_saturation, command=self._change_HSV)
        self._S_saturation.grid(row=0, column=0, columnspan=2, sticky=E)

        self._SV_saturationD = StringVar(value="0")
        self._S_saturationD = Scale(self._LF_saturation, from_=0, to=100, orient=HORIZONTAL, variable=self._SV_saturationD)
        self._S_saturationD.grid(row=1, column=0, columnspan=2, sticky=E)


        """#################### LUMINOSITY ####################"""
        self._LF_value = LabelFrame(parent, text="V")
        self._LF_value.grid(row=2, column=0, sticky=(E, W))

        self._SV_value = StringVar(value="100")
        self._S_value = Scale(self._LF_value, from_=0, to=100, orient=HORIZONTAL, variable=self._SV_value, command=self._change_HSV)
        self._S_value.grid(row=0, column=0, columnspan=2, sticky=E)

        self._SV_valueD = StringVar(value="0")
        self._S_valueD = Scale(self._LF_value, from_=0, to=100, orient=HORIZONTAL, variable=self._SV_valueD)
        self._S_valueD.grid(row=1, column=0, columnspan=2, sticky=E)


        """#################### Speed ####################"""
        self._LF_SPEED = LabelFrame(parent, text="T")
        self._LF_SPEED.grid(row=3, column=0, sticky=(E, W))

        self._SV_SPEED = StringVar(value="60")
        self._S_SPEED = Scale(self._LF_SPEED, from_=10, to=500, orient=HORIZONTAL, variable=self._SV_SPEED)
        self._S_SPEED.grid(row=0, column=0, columnspan=2, sticky=E)

        self._B_SPEED_Reset = Button(self._LF_SPEED, command=self.resetSpeed, text="Reset speed")
        self._B_SPEED_Reset.grid(row=1, column=0, sticky=E)

        """#################### Interpolation ####################"""
        self._LF_INTERPO = LabelFrame(parent, text="I")
        self._LF_INTERPO.grid(row=4, column=0, sticky=(E, W))

        self._SV_INTERPO = StringVar(value="100")
        self._S_INTERPO = Scale(self._LF_INTERPO, from_=10, to=100, orient=HORIZONTAL, variable=self._SV_INTERPO)
        self._S_INTERPO.grid(row=0, column=0, columnspan=2, sticky=E)

    def resetSpeed(self):
        self._S_SPEED.set(5)

    def _change_HSV(self, e=None):
        self._color = Color.fromHSV(
            float(self._SV_hue.get()),
            float(self._SV_saturation.get())/100.0,
            float(self._SV_value.get())/100.0)

        self.mainFrame.configure(background=self._color.toHex())

    def update(self):
        #self._SV_SPEED.get()) != self._parent.getSpeed():
        if int(self._parent.getSpeed()) != 5: 
            self._parent.setSpeed(5) #int(self._SV_SPEED.get()))
            
        if self._controller.nbLeds is not None and self._controller.nbLeds > len(self._colors):
            self._colors = [Color() for _ in range(self._controller.nbLeds)]
            
        if self.iupdateCounter != 0:
            for i in range(self._controller.nbLeds):
                self._colors[i] = self.interpolate(self._colors[i], self.newColors[i], 0.05)
                tmp = Color.fromList(self._colors[i].toList()).enhance(gr=0.60, br=0.45, bg=0.25)
                self._controller.buffer[i] =  tmp.toList()
            self._controller.send()
            self.iupdateCounter -= 1
           
        else:
        


            hue  = float( self._SV_hue.get())
            hueD = float(self._SV_hueD.get())
            HueValues = ( hue , (hue-hueD)%360 )

            saturation  = float( self._SV_saturation.get())
            saturationD = float(self._SV_saturationD.get())
            SatValues = ( saturation, saturation-saturationD  )

            value  = float( self._SV_value.get())
            valueD = float(self._SV_valueD.get())
            ValValues = ( value, value-valueD  )
            
            self.newColors.clear()
            for i in range(self._controller.nbLeds):
                self.newColors.append(Color.fromHSV(
                    randrange(min(*HueValues), max(*HueValues)),
                    randrange(min(*SatValues), max(*SatValues)) / 100.0,
                    randrange(min(*ValValues), max(*ValValues)) / 100.0))
            
            self.iupdateCounter = int(self._SV_SPEED.get()) // 5