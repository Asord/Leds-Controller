from AsemcoAPI.TkXbox.XboxTkWindow import XboxTkWindow
from AsemcoAPI.TkXbox.Defines import *
from AsemcoAPI.Tools.Json import loadf
from AsemcoAPI.Tools.Scalling import centerGeometryS

from Utilities.ArduinoController import ArduinoController
from Utilities.Colors import Color
from Utilities.JoyTable import JoyTable

from math import atan2, degrees


class MainWindow(XboxTkWindow):
    def __init__(self):
        XboxTkWindow.__init__(self, "gui/MainWindow.json", "LedsController X")

        self.settings = loadf("settings.json")
        if "geometry" in self.settings:
            self.geometry(centerGeometryS(self.settings["geometry"]))
        if "alpha" in self.settings:
            self.wm_attributes("-alpha", self.settings["alpha"])
        if "notitle" in self.settings:
            self.overrideredirect(1)
        if "background" in self.settings:
            self.configure(background=self.settings["background"])

        self.controller = ArduinoController()
        self.controller.nbLeds = self.settings["numberOfLeds"]
        self.controller.clear()


        self.isColorChooserEnabled = False
        self.isValueChooserEnabled = False

        self.color = Color()
        self.__colorHSV = [0.0, 1.0, 1.0]
        self.colorFrame = self.widgets["frame_main"]

        self.__leftJoy  = JoyTable(self.leftJoystick)
        self.__rightJoy = JoyTable(self.rightJoystick)

        # color selector
        self.joybind(JOY_RIGHT_THUMB_X, self.__rightJoy.setX)
        self.joybind(JOY_RIGHT_THUMB_Y, self.__rightJoy.setY)

        # saturation/value selector
        self.joybind(JOY_LEFT_THUMB_X, self.__leftJoy.setX)
        self.joybind(JOY_LEFT_THUMB_Y, self.__leftJoy.setY)

        self.joybind(JOY_LEFT_TRIGER, self.leftTrigger)
        self.joybind(JOY_RIGHT_TRIGER, self.rightTrigger)

        self.protocol("WM_DELETE_WINDOW", self._handleClose)

        self._StartXHandler()

    def updateColor(self):
        if self.controller.isConnected():
            self.color.enhance(gr=0.60, br=0.45, bg=0.25)

            for n in range(self.controller.nbLeds):
                self.controller.buffer[n] = self.color.toList()
            self.controller.send()

        self.after(100, self.updateColor)

    def rightJoystick(self, joyTable):
        if self.isColorChooserEnabled:

            rad = atan2(joyTable.y, joyTable.x)
            deg = 90-degrees(rad)
            if deg < 0: deg += 360.0

            self.__colorHSV[0] = deg
            self.colorFrame.configure(bg=self.color.toHex())

            self.color = Color.fromHSV(*self.__colorHSV)
            self.colorFrame.configure(bg=self.color.toHex())

    def leftJoystick(self, joyTable):
        if self.isColorChooserEnabled:

            rad = atan2(joyTable.y, joyTable.x)
            deg = 90-degrees(rad)
            if deg < 0: deg += 360.0

            val = deg/360.0

            if self.isValueChooserEnabled:
                self.__colorHSV[2] = val
            else:
                self.__colorHSV[1] = val

            self.color = Color.fromHSV(*self.__colorHSV)
            self.colorFrame.configure(bg=self.color.toHex())


    def leftTrigger(self, value):
        if value > 0.1:
            self.isValueChooserEnabled = True
        else:
            self.isValueChooserEnabled = False

    def rightTrigger(self, value):
        if value > 0.1:
            self.isColorChooserEnabled = True
        else:
            self.isColorChooserEnabled = False

    def _handleClose(self):
        self._controller.clear()
        self._controller.send()
        self._controller.destroy()
        self.destroy()

if __name__ == '__main__':
    mainWindow = MainWindow()
    mainWindow.mainloop()