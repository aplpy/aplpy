import os
import sys
from astropy.extern import six

if six.PY3:
    from io import BytesIO as StringIO
else:
    from StringIO import StringIO

import numpy as np
from astropy.tests.helper import pytest

from .. import FITSFigure

FORMATS = [None, 'png', 'pdf', 'eps', 'ps', 'svg']


def is_format(filename, format):
    if isinstance(filename, six.string_types):
        f = open(filename, 'rb')
    else:
        f = filename
    if format == 'png':
        return f.read(8) == b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a'
    elif format == 'pdf':
        return f.read(4) == b'\x25\x50\x44\x46'
    elif format == 'eps':
        return f.read(23) == b'%!PS-Adobe-3.0 EPSF-3.0'
    elif format == 'ps':
        return f.read(14) == b'%!PS-Adobe-3.0'
    elif format == 'svg':
        from xml.dom import minidom
        return minidom.parse(f).childNodes[2].attributes['xmlns'].value == 'http://www.w3.org/2000/svg'
    else:
        raise Exception("Unknown format: %s" % format)


@pytest.mark.parametrize(('format'), FORMATS)
def test_write_png(tmpdir, format):
    filename = os.path.join(str(tmpdir), 'test_output.png')
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.show_grayscale()
    try:
        f.save(filename, format=format)
    except TypeError:
        pytest.xfail()
    finally:
        f.close()
    if format is None:
        assert is_format(filename, 'png')
    else:
        assert is_format(filename, format)


@pytest.mark.parametrize(('format'), FORMATS)
def test_write_pdf(tmpdir, format):
    filename = os.path.join(str(tmpdir), 'test_output.pdf')
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.show_grayscale()
    try:
        f.save(filename, format=format)
    except TypeError:
        pytest.xfail()
    finally:
        f.close()
    if format is None:
        assert is_format(filename, 'pdf')
    else:
        assert is_format(filename, format)


@pytest.mark.parametrize(('format'), FORMATS)
def test_write_eps(tmpdir, format):
    filename = os.path.join(str(tmpdir), 'test_output.eps')
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.show_grayscale()
    try:
        f.save(filename, format=format)
    except TypeError:
        pytest.xfail()
    finally:
        f.close()
    if format is None:
        assert is_format(filename, 'eps')
    else:
        assert is_format(filename, format)


@pytest.mark.parametrize(('format'), FORMATS)
def test_write_stringio(tmpdir, format):
    s = StringIO()
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.show_grayscale()
    try:
        f.save(s, format=format)
    except TypeError:
        pytest.xfail()
    finally:
        f.close()
    try:
        s.seek(0)
    except ValueError:
        if format == 'svg' and sys.version_info[:2] >= (3, 3):
            pytest.xfail()
        else:
            raise
    if format is None:
        assert is_format(s, 'png')
    else:
        assert is_format(s, format)
