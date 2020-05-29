def linearSteps(number, nbSlices, precision=1):
    
    if number == 0:
        _steps = [0 for _ in range(nbSlices)]
        
    else:    
        _nbFrames = nbSlices - 1
        
        numberNormalized = int(number*precision)
        _dIncrement = int(numberNormalized / _nbFrames)
        
        _steps = [k/precision for k in range(0, numberNormalized, _dIncrement)]

        if numberNormalized % _nbFrames == 0: _steps.append(numberNormalized/precision)
        else: _steps[-1] = numberNormalized/precision

    return _steps

def scale(oldMin, oldMax, newMin, newMax, value):
    return ((value-oldMin) / (oldMax-oldMin)) * (newMax-newMin)+newMin
