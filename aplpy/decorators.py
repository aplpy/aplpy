import threading
mydata = threading.local()
mydata.nesting = 0

def auto_refresh(f):
    def wrapper(*args, **kwargs):
        if 'refresh' in kwargs:
            refresh = kwargs.pop('refresh')
        else:
            refresh = True
        mydata.nesting += 1
        try:
            f(*args, **kwargs)
        finally:
            mydata.nesting -= 1
            if hasattr(args[0], '_figure'):
                if refresh and mydata.nesting == 0 and args[0]._figure._auto_refresh:
                    args[0]._figure.canvas.draw()
    wrapper.__doc__ = f.__doc__
    wrapper.__name__ = f.__name__
    return wrapper
