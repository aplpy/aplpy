from __future__ import absolute_import, print_function, division

import threading

from .decorator import decorator


mydata = threading.local()


def auto_refresh(f):
    return decorator(_auto_refresh, f)


def _auto_refresh(f, *args, **kwargs):
    if 'refresh' in kwargs:
        refresh = kwargs.pop('refresh')
    else:
        refresh = True
    # The following is necessary rather than using mydata.nesting = 0 at the
    # start of the file, because doing the latter caused issues with the Django
    # development server.
    mydata.nesting = getattr(mydata, 'nesting', 0) + 1
    try:
        return f(*args, **kwargs)
    finally:
        mydata.nesting -= 1
        if hasattr(args[0], '_figure'):
            if refresh and mydata.nesting == 0 and args[0]._parameters.auto_refresh:
                args[0]._figure.canvas.draw()


doc = {}

doc['size'] = '''size : str or int or float, optional
    The size of the font. This can either be a numeric value (e.g.
    12), giving the size in points, or one of 'xx-small', 'x-small',
    'small', 'medium', 'large', 'x-large', or 'xx-large'.
    '''

doc['weight'] = '''weight : str or int or float, optional
    The weight (or boldness) of the font. This can either be a numeric
    value in the range 0-1000 or one of 'ultralight', 'light', 'normal',
    'regular', 'book', 'medium', 'roman', 'semibold', 'demibold', 'demi',
    'bold', 'heavy', 'extra bold', 'black'.
    '''

doc['stretch'] = '''stretch : str or int or float, optional
    The stretching (spacing between letters) for the font. This can either
    be a numeric value in the range 0-1000 or one of 'ultra-condensed',
    'extra-condensed', 'condensed', 'semi-condensed', 'normal',
    'semi-expanded', 'expanded', 'extra-expanded' or 'ultra-expanded'.
    '''

doc['family'] = '''family : str, optional
    The family of the font to use. This can either be a generic font
    family name, either 'serif', 'sans-serif', 'cursive', 'fantasy', or
    'monospace', or a list of font names in decreasing order of priority.
    '''

doc['style'] = '''style : str, optional
    The font style. This can be 'normal', 'italic' or 'oblique'.
    '''

doc['variant'] = '''variant : str, optional
    The font variant. This can be 'normal' or 'small-caps'
    '''


def fixdocstring(func):

    lines = func.__doc__.split('\n')

    for i, line in enumerate(lines):
        if 'common:' in line:
            break

    header = lines[:i]

    footer = lines[i + 1:]

    indent = lines[i].index('common:')

    common = []
    for item in lines[i].split(':')[1].split(','):
        if item.strip() in doc:
            common.append(" " * indent + doc[item.strip()].replace('\n', '\n' + " " * indent))

    docstring = "\n".join(header + common + footer)

    func.__doc__ = docstring

    return func
