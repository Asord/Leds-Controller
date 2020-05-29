from serial import Serial, SerialTimeoutException, SerialException
from serial.tools.list_ports import comports
from time import time


DEFAULTCARDNAME = "Arduino Uno"

class ArduinoController:
    def __init__(self, cardName=DEFAULTCARDNAME):


        self.buffer = []
        self.vars = {}

        self.nbLeds = 21

        self._cardName = cardName
        self._header = b"Ada"

        self._serial = None
        self._lpack = None
        self._isConnected = False
        self._connectionType = ""

        self._createHeader()
        self._connect()

    def _createHeader(self):
        self._header += bytes([(self.nbLeds - 1) >> 8])
        self._header += bytes([(self.nbLeds - 1) & 0xff])
        self._header += bytes([self._header[3] ^ self._header[4] ^ 0x55])

    def __findController(self):
        ports = comports()

        portName = ""
        for port in ports:
            if self._cardName in port.description:
                portName = port.device
                break

        return portName

    def isConnected(self):
        return self._isConnected

    def _connect(self):
        portName = self.__findController()
        if portName == "":
            print("Can't found any ports...")
            return

        try:
            self._serial = Serial(portName, 115200)
        except FileNotFoundError:
            print("Serial at port %s can't be found..." % portName)
            return -1
        except SerialException:
            print("The connection to the serial at port %s has  been interupted..." % portName)
            return -1

        start = time()
        while time() - start < 5:  # 5s timeout
            data = self._serial.readline()
            if data == b"Ada\n":
                self._isConnected = True
                self._connectionType = "direct"
                return 0

        print("The serial at port %s didn't send the magic word. Can't connect...", portName)
        return -2

    def _disconect(self):
        self._isConnected = False
        if self._connectionType == "direct":
            self._serial = None
        else:
            self._lpack.unlock()

    def destroy(self):
        if self._serial is not None:
            self.clear()
            self.send()
            self._serial.close()

        self._serial = None
        self._isConnected = False

    def ___del__(self):
        self.destroy()

    def moderate(self, coefR=1.0, coefG=1.0, coefB=1.0):
        cR = coefR if 0 <= coefR <= 1.0 else 1.0
        cG = coefG if 0 <= coefG <= 1.0 else 1.0
        cB = coefB if 0 <= coefB <= 1.0 else 1.0

        for col in self.buffer:
            col[0] = int(col[0] * cR)
            col[1] = int(col[1] * cG)
            col[2] = int(col[2] * cB)

    def __sendDirect(self):
        if self._serial is None:
            e = self._connect()
            if e != 0: return

        data = self._header

        if len(self.buffer) < self.nbLeds:
            for _ in range(len(self.buffer), self.nbLeds):
                self.buffer.append([0, 0, 0])

        for p in range(self.nbLeds):
            data += bytes(self.buffer[p])

        try:
            self._serial.write(data)
        except SerialTimeoutException:
            self._disconect()
        except SerialException:
            self._disconect()

    def __sendSocket(self):
        for i in range(self.nbLeds):
            col = self.buffer[i]
            r = col[0]
            g = col[1]
            b = col[2]
            self._lpack.setColor(i, r, g, b)

    def send(self):
        if self._connectionType == "direct":
            self.__sendDirect()
        elif self._connectionType == "socket":
            self.__sendSocket()

    def clear(self):
        self.buffer.clear()
        for i in range(self.nbLeds):
            self.buffer.append([0, 0, 0])
