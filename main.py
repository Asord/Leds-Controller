from LedsInterface import Interface, singleColor_module, fromFile_module, hsvrgb_module

if __name__ == '__main__':
    i = Interface()

    i.registerModule("Single color", singleColor_module)
    i.registerModule("From file"   ,    fromFile_module)
    i.registerModule("HSV-RGB"     ,      hsvrgb_module)
    
    i.mainloop()