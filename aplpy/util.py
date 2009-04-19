import numpy as np

def smart_range(array):
    
    array.sort()
    
    minval = 360.
    i1 = 0
    i2 = 0
    
    for i in range(0,np.size(array)-1):
        if 360.-abs(array[i+1]-array[i]) < minval:
            minval = 360.-abs(array[i+1]-array[i])
            i1 = i+1
            i2 = i
    
    if(max(array)-min(array) < minval):
        i1 = 0
        i2 = np.size(array)-1
    
    x_min = array[i1]
    x_max = array[i2]
    
    if(x_min > x_max):
        x_min = x_min - 360.
    
    return x_min,x_max

def smart_round_x(x):
    x = x / 15.
    if x > 1:
        x = round(x,0)
    else:
        x = x * 60.
        if x > 1:
            x = round(x,0) / 60.
        else:
            x = x * 60.
            if x > 1:
                x = round(x,0) / 3600.
            else:
                x = x * 100.
                if x > 1:
                    x = round(x,0) / 360000.
                else:
                    x = x / 100.
    x = x * 15.
    return x

def smart_round_y(y):
    if y > 1:
        y = round(y,0)
    else:
        y = y * 60.
        if y > 1:
            y = round(y,0) / 60.
        else:
            y = y * 60.
            if y > 1:
                y = round(y,0) / 3600.
            else:
                y = y * 100.
                if y > 1:
                    y = round(y,0) / 360000.
                else:
                    y = y / 100.
    return y

def complete_range(xmin,xmax,spacing):
    if(xmax-xmin < 1):
        spacing = 10
    xstep = (xmax - xmin) / float(spacing)
    r = np.arange(xmin,xmax,xstep)
    if(np.any(r>=xmax)):
        return r
    else:
        return np.hstack([r,xmax])