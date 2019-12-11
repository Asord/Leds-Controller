from tkinter import Frame, filedialog, Button, StringVar, Spinbox, HORIZONTAL, Scale
from tkinter import E, W
from png import Reader

from LedsInterface.Utilities.Colors import Color

from LedsInterface.base import baseModule

class fromFile_module(baseModule):
    def __init__(self, parent):
        baseModule.__init__(self, parent)

        self._s_fileName = ""
        self._b_fileLoaded = False
        self._s_fileType = ""

        self.__nbleds = 0
        self.__nbframes = 0
        self.__data = []

        self.__colorSH = Color.zero()
        self.__rainbowHue = 0.0
        self.__x = 0

        self.mainFrame = Frame(parent)
        self.mainFrame.grid(sticky=(E, W))
        self.populateInterface(self.mainFrame)

    def populateInterface(self, parent):
        """
        populate interface
        """
        """#################### Rainbow Speed ####################"""
        self._SV_rainbowSpeed = StringVar(value="30")
        self._S_rainbowSpeed = Scale(parent, from_=0, to=100, orient=HORIZONTAL, variable=self._SV_rainbowSpeed)
        self._S_rainbowSpeed.grid(row=0, column=0, columnspan=2, sticky=(E, W))

        self._B_rainbowSpeed_Reset = Button(parent, command=self.resetRainbowSpeed, text="reset rainbow speed")
        self._B_rainbowSpeed_Reset.grid(row=0, column=2)

        """#################### Speed ####################"""
        self._SV_SPEED = StringVar(value="60")
        self._S_SPEED = Scale(parent, from_=10, to=500, orient=HORIZONTAL, variable=self._SV_SPEED)
        self._S_SPEED.grid(row=1, column=0, columnspan=2, sticky=(E, W))

        self._B_SPEED_Reset = Button(parent, command=self.resetSpeed, text="Reset speed")
        self._B_SPEED_Reset.grid(row=1, column=2)

        """#################### File selecter ####################"""
        self._B_selectFile = Button(parent, command=self._selectFile, text="Select file")
        self._B_selectFile.grid(row=2, column=0)

    def resetRainbowSpeed(self):
        self._S_rainbowSpeed.set(30)

    def resetSpeed(self):
        self._S_SPEED.set(60)

    def __readPngFile(self):
        with open(self._s_file, "rb") as fs:
            _reader = Reader(file=fs)
            _data = _reader.read()

            _colorarray = []
            for frame in list(_data[2]):
                framearray = list(frame)
                _colorarray.append([framearray[x:x + 3] for x in range(0, len(framearray), 3)])

            self.__nbleds   = _data[0]
            self.__nbframes = _data[1]
            self.__data     = _colorarray

    def _selectFile(self):
        self._s_file = filedialog.askopenfilename(initialdir=".",
                                                  title="Select file",
                                                  filetypes=(("png files", "*.png"),))

        self._s_fileType = self._s_file.split("_")[1].replace(".png", "")

        if self._s_fileType not in ["rnb", "fi", "sh"]:
            self._s_file = ""
            self._s_fileType = ""
            self._b_fileLoaded = False
        else:
            self.__readPngFile()
            self._controller.nbLeds = self.__nbleds
            self._b_fileLoaded = True
            self.__rainbowHue = 0.0
            self.__x = 0

        self._parent.resetSpeed()
        self._S_SPEED.set(int(self._parent.getSpeed()))

    def _updateRNB(self):
        self._controller.clear()
        color = Color.fromHSV(self.__rainbowHue, 1.0, 1.0).mul([1.0, 0.42, 0.3])

        for y in range(self.__nbleds):
            col = color * Color.fromList(self.__data[self.__x][y])
            self._controller.buffer[y] = col.toList()

        self.__rainbowHue += int(self._SV_rainbowSpeed.get()) / 10.0
        self.__rainbowHue %= 360.0
        self._controller.send()

    def _updateFI(self):
        self._controller.clear()

        for y in range(self.__nbleds):
            col = Color.fromList(self.__data[self.__x][y])
            col.mul([1.0, 0.42, 0.3])
            self._controller.buffer[y] = col.toList()

        self._controller.send()

    def _updateSH(self):
        if self.__x == 0:
            self.__colorSH = Color.randomColor().mul([1.0, 0.42, 0.3])

        self._controller.clear()

        for y in range(self.__nbleds):
            col = self.__colorSH * Color.fromList(self.__data[self.__x][y])
            self._controller.buffer[y] = col.toList()

        self._controller.send()

    def __wishedSpeed(self):
        return int(self._SV_SPEED.get())

    def update(self):
        if self._b_fileLoaded:
            if  self.__wishedSpeed() != self._parent.getSpeed():
                self._parent.setSpeed(self.__wishedSpeed())

            if self._s_fileType == "rnb":
                self._updateRNB()
            elif self._s_fileType == "fi":
                self._updateFI()
            elif self._s_fileType == "sh":
                self._updateSH()
            else:
                print("Error while trying to get file type.")

            self.__x = self.__x + 1 if (self.__x+1 < self.__nbframes) else 0
