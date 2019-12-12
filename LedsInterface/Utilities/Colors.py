from math import floor
from random import randint


class Color:
    def __init__(self, red=0, gre=0, blu=0):

        self._red = 0
        self._green = 0
        self._blue = 0

        if 0 <= red <= 255:
            self._red = int(red)
        if 0 <= gre <= 255:
            self._green = int(gre)
        if 0 <= blu <= 255:
            self._blue = int(blu)

    def red(self):
        return self._red

    def green(self):
        return self._green

    def blue(self):
        return self._blue

    @classmethod
    def fromHex(cls, hexVal):
        hexValue = hexVal.replace("#", "")
        r = int(hexValue[0:2], 16)
        g = int(hexValue[2:4], 16)
        b = int(hexValue[4:6], 16)
        return cls(r, g, b)

    @classmethod
    def fromHSV(cls, h, s, v):
        h = float(h)
        s = float(s)
        v = float(v)
        h60 = h / 60.0
        h60f = floor(h60)
        hi = int(h60f) % 6
        f = h60 - h60f
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        r, g, b = 0, 0, 0
        if hi == 0:
            r, g, b = v, t, p
        elif hi == 1:
            r, g, b = q, v, p
        elif hi == 2:
            r, g, b = p, v, t
        elif hi == 3:
            r, g, b = p, q, v
        elif hi == 4:
            r, g, b = t, p, v
        elif hi == 5:
            r, g, b = v, p, q
        r, g, b = int(r * 255), int(g * 255), int(b * 255)

        return cls(r, g, b)

    @classmethod
    def fromList(cls, col):
        return cls(*col)

    @classmethod
    def random(cls):
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        return cls(r, g, b)

    @classmethod
    def randomColor(cls):
        return cls.fromHSV(randint(0, 360), 1.0, 1.0)


    @classmethod
    def zero(cls):
        return cls(0, 0, 0)

    @classmethod
    def copy(cls, col):
        r, g, b = col.toTuple()
        cls(r, g, b)

    def __add__(self, other):
        if type(other) is Color:
            r = (self._red + other.red()) % 256
            g = (self._green + other.green()) % 256
            b = (self._blue + other.blue()) % 256

            return Color(r, g, b)

    def __mul__(self, other):
        r = self._red
        g = self._green
        b = self._blue

        if type(other) is int or type(other) is float:
            r *= other
            g *= other
            b *= other

        if type(other) is Color:
            _or = other._red / 256
            _og = other._green / 256
            _ob = other._blue / 256

            r *= _or
            g *= _og
            b *= _ob

        return Color(r % 256, g % 256, b % 256)

    def mul(self, other):
        r = self._red * other[0]
        g = self._green * other[1]
        b = self._blue * other[2]

        self.set(r, g, b)

        return self
        
    def enhance(self, rg=0.0, rb=0.0, gr=0.0, gb=0.0, br=0.0, bg=0.0):
        norms = list(self.normalize())
        norms[0] = norms[0] - rg * norms[1] - rb * norms[2]
        norms[1] = norms[1] - gr * norms[0] - gb * norms[2]
        norms[2] = norms[2] - br * norms[0] - bg * norms[1]
        self.setNormalized(*norms)
       

    def grayScale(self):
        gray = (self._red+self._green+self._blue) / 3
        return 1- gray/255

    def set(self, red, gre, blu):
        if 0 <= red <= 255:
            self._red = int(red)
        if 0 <= gre <= 255:
            self._green = int(gre)
        if 0 <= blu <= 255:
            self._blue = int(blu)
        return self

    def half(self):
        self._red //= 2
        self._green //= 2
        self._blue //= 2
        return self

        
    def normalize(self):
        return self._red/255.0, self._green/255.0, self._blue/255.0
        
    def setNormalized(self, red, green, blue):
        norms = [red, green, blue]
        
        for normID in range(len(norms)):
            if   norms[normID] < 0: norms[normID] = 0
            elif norms[normID] > 1: norms[normID] = 1
            
        self._red   = int(norms[0]*255)
        self._green = int(norms[1]*255)
        self._blue  = int(norms[2]*255)

    def toHSV(self):
        r, g, b = self.normalize()
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx - mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g - b) / df) + 360) % 360
        elif mx == g:
            h = (60 * ((b - r) / df) + 120) % 360
        elif mx == b:
            h = (60 * ((r - g) / df) + 240) % 360

        if mx == 0:
            s = 0
        else:
            s = df / mx
        v = mx
        return h, s, v

    def toHex(self):
        rh = format(self._red, '02x')
        gh = format(self._green, '02x')
        bh = format(self._blue, '02x')
        return '#%s%s%s' % (rh, gh, bh)

    def toInt(self):
        integer = self._blue
        integer += self._green << 8
        integer += self._red << 16
        return integer

    def toList(self):
        return [self._red, self._green, self._blue]

    def toListLED(self):
        return [self._red, self._blue, self._green]

    def __repr__(self):
        return "color (%s, %s, %s)" % (self._red, self._green, self._blue)

    def __str__(self):
        return self.__repr__()



class Colors:
    black = Color(0, 0, 0)
    white = Color(255, 255, 255)

    red = Color(255, 0, 0)
    blue = Color(0, 255, 0)
    green = Color(0, 0, 255)

    yellow = Color(255, 0, 255)
    cyan = Color(0, 255, 255)
    magenta = Color(255, 255, 0)
