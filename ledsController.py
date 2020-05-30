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

        self.currentEffect = 0 # 0: Color 1: Rainbow 2: snake

        self.isColorChooserEnabled = False
        self.isValueChooserEnabled = False

        self.color = Color(255, 0, 0)
        self.__colorHSV = [0.0, 1.0, 1.0]
        self.colorFrame = self.widgets["frame_up"]
        self.previewFrame = self.widgets["frame_down"]

        self.modificatorSpeed = 1.0

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

        self.xbind(JOY_LB, lambda: self.switchEffect(-1))
        self.xbind(JOY_RB, lambda: self.switchEffect( 1))

        self.xbind(JOY_DOWN, lambda: self.changeModificatorSpeed(-1))
        self.xbind(JOY_UP  , lambda: self.changeModificatorSpeed( 1))
        self.xbind(JOY_B   , self._handleClose)

        self.protocol("WM_DELETE_WINDOW", self._handleClose)

        self._StartXHandler()

        self.updateColor()

    def changeModificatorSpeed(self, modificator):
        if modificator == -1:
            if self.modificatorSpeed > 0.09:
                self.modificatorSpeed -= 0.1
        elif modificator == 1:
            if self.modificatorSpeed < 5.0:
                self.modificatorSpeed += 0.1

    def switchEffect(self, direction):
        self.color = Color(255, 0, 0)
        self.__colorHSV = [0.0, 1.0, 1.0]

        if direction == -1:
            if self.currentEffect == 0:
                self.currentEffect = 2
            else:
                self.currentEffect -= 1
        elif direction == 1:
            if self.currentEffect == 2:
                self.currentEffect = 0
            else:
                self.currentEffect += 1

    def __sendSingleColorToAll(self, color):
        colorToSend = Color.copy(color).enhance(gr=0.60, br=0.45, bg=0.25)
        colorToSendList = colorToSend.toList()
        for n in range(self.controller.nbLeds):
            self.controller.buffer[n] = colorToSendList

        self.previewFrame.configure(bg=colorToSend.toHex())

    def updateColor(self):
        if self.controller.isConnected():
            if self.currentEffect == 0:
                self.__sendSingleColorToAll(self.color)

            elif self.currentEffect == 1:

                h, s, v = self.__colorHSV
                for n in range(self.controller.nbLeds):
                    self.controller.buffer[n] = Color().fromHSV(h, s, v).enhance(gr=0.60, br=0.45, bg=0.25).toList()
                    h -= self.modificatorSpeed

                self.__colorHSV[0] += self.modificatorSpeed
                self.color = Color.fromHSV(*self.__colorHSV)
                self.previewFrame.configure(bg=self.color.toHex())

            elif self.currentEffect == 2:
                self.__sendSingleColorToAll(self.color)
                self.__colorHSV[0] += self.modificatorSpeed
                self.color = Color.fromHSV(*self.__colorHSV)

            self.controller.send()

        self.after(100, self.updateColor)

    def rightJoystick(self, joyTable):
        if self.currentEffect == 0 and self.isColorChooserEnabled:

            rad = atan2(joyTable.y, joyTable.x)
            deg = 90-degrees(rad)
            if deg < 0: deg += 360.0

            self.__colorHSV[0] = deg
            self.colorFrame.configure(bg=self.color.toHex())

            self.color = Color.fromHSV(*self.__colorHSV)
            self.colorFrame.configure(bg=self.color.toHex())

    def leftJoystick(self, joyTable):
        if self.currentEffect == 0 and self.isColorChooserEnabled:

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
        if  self.currentEffect == 0 and value > 0.1:
            self.isValueChooserEnabled = True
        else:
            self.isValueChooserEnabled = False

    def rightTrigger(self, value):
        if self.currentEffect == 0 and value > 0.1:
            self.isColorChooserEnabled = True
        else:
            self.isColorChooserEnabled = False

    def _handleClose(self):
        self.controller.clear()
        self.controller.send()
        self.controller.destroy()
        self.destroy()

if __name__ == '__main__':
    mainWindow = MainWindow()
    mainWindow.mainloop()