class JoyTable:
    def __init__(self, onDefinedCallable=None):
        self.x = 0.0
        self.y = 0.0
        self.s = 0

        self.callable = onDefinedCallable

    def setX(self, val):
        if not self.s & 1:
            self.x = val
            self.s |= 1

        if self.isSet():
            self.callback()

    def setY(self, val):
        if not self.s & 2:
            self.y = val
            self.s |= 2

        if self.isSet():
            self.callback()

    def isSet(self):
        return self.s == 3

    def callback(self):
        if self.callable is not None:
            self.callable(self)
        self.s = 0

    def __str__(self):
        return "x(%f) | y(%f) | actual state: %d" % (self.x, self.y, self.s)