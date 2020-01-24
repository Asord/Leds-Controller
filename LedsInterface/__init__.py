from LedsInterface.base import baseInterface
from LedsInterface.fromFile_module import fromFile_module
from LedsInterface.singleColor_module import singleColor_module
from LedsInterface.hsvrgb_module import hsvrgb_module
from LedsInterface.shades_module import shades_module

class Interface(baseInterface):
    def __init__(self):
        baseInterface.__init__(self)
