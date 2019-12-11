from tkinter import Tk, Radiobutton
from tkinter import E, W
from tkinter.ttk import Notebook

from LedsInterface.Utilities.ArduinoController import ArduinoController

class baseModule:
    def __init__(self, parent):
        self._parent = parent

        self._controller = None

    def linkController(self, controller):
        self._controller = controller

    @staticmethod
    def _safeGetValueFromSlider(slider, part, default):
        try:
            value = int(slider.get()) / part
        except ValueError:
            value = default
        return value

    @staticmethod
    def _createToggle(parent, offText, onText, variable, ):
        defaultVars = {"indicatoron": False, "width": 10, "variable": variable}
        return [
            Radiobutton(parent, text=offText, value="off", **defaultVars),
            Radiobutton(parent, text=onText, value="on", **defaultVars)
        ]

    def update(self):
        raise NotImplementedError("Update must be implemented on derived classes")

    def populateInterface(self, parentFrame):
        raise NotImplementedError("populateInterface must be implemented on derived classes")


class baseInterface(Tk):
    def __init__(self):
        Tk.__init__(self)

        self._controller = ArduinoController()
        self._controller.nbLeds = 21
        self._controller.clear()

        self._notebook = Notebook(self)
        self._notebook.grid(sticky=(E, W))

        self.__modules = {}

        self.__defaultSpeed = 60
        self._updateSpeed = self.__defaultSpeed

        self.protocol("WM_DELETE_WINDOW", self._handleClose)
        self.__update()

    def setSpeed(self, speed):
        if 10 <= speed <= 500:
            self._updateSpeed = speed
        else:
            self._updateSpeed = self.__defaultSpeed

    def getSpeed(self):
        return self._updateSpeed

    def resetSpeed(self):
        self._updateSpeed = self.__defaultSpeed

    def registerModule(self, name, obj):
        self.__modules[name] = obj(self)
        self.__modules[name].linkController(self._controller)
        self._notebook.add(self.__modules[name].mainFrame, text=name)


    def _handleClose(self):
        self._controller.clear()
        self._controller.send()
        self._controller.destroy()
        self.destroy()

    def _getCurrentTabName(self):
        return self._notebook.tab(self._notebook.select(), "text")

    def __update(self):
        if len(self.__modules) > 0:
            self.__modules[self._getCurrentTabName()].update()
        self.after(self._updateSpeed, self.__update)
