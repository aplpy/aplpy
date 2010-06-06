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

import string

doc = {}

doc['size'] = '''*size*:
    The size of the font. This can either be a numeric value (e.g.
    12), giving the size in points, or one of ‘xx-small’, ‘x-small’,
    ‘small’, ‘medium’, ‘large’, ‘x-large’, or ‘xx-large’.
    '''

doc['weight'] = '''*weight*:
    The weight (or boldness) of the font. This can either be a numeric
    value in the range 0-1000 or one of ‘ultralight’, ‘light’, ‘normal’,
    ‘regular’, ‘book’, ‘medium’, ‘roman’, ‘semibold’, ‘demibold’, ‘demi’,
    ‘bold’, ‘heavy’, ‘extra bold’, ‘black’.
    '''

doc['stretch'] = '''*stretch*:
    The stretching (spacing between letters) for the font. This can either
    be a numeric value in the range 0-1000 or one of ‘ultra-condensed’,
    ‘extra-condensed’, ‘condensed’, ‘semi-condensed’, ‘normal’,
    ‘semi-expanded’, ‘expanded’, ‘extra-expanded’ or ‘ultra-expanded’.
    '''

doc['family'] = '''*family*:
    The family of the font to use. This can either be a generic font
    family name, either ‘serif’, ‘sans-serif’, ‘cursive’, ‘fantasy’, or
    ‘monospace’, or a list of font names in decreasing order of priority.
    '''

doc['style'] = '''*style*:
    The font style. This can be ‘normal’, ‘italic’ or ‘oblique’.
    '''

doc['variant'] = '''*variant*:
    The font variant. This can be ‘normal’ or ‘small-caps’
    '''

def fixdocstring(func):

    lines = func.__doc__.split('\n')

    for i, line in enumerate(lines):
        if 'common:' in line:
            break

    header = lines[:i]

    footer = lines[i+1:]

    indent = lines[i].index('common:') + 4

    common = []
    for item in lines[i].split(':')[1].split(','):
        if item.strip() in doc:
            common.append(" " * indent + doc[item.strip()].replace('\n','\n' + " "*indent))

    docstring = string.join(header + common + footer, "\n")

    func.__doc__ = docstring

    return func