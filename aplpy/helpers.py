from __future__ import absolute_import, print_function, division

from distutils.version import LooseVersion
from astropy import __version__

__all__ = ['ASTROPY_LT_30', 'ASTROPY_LT_31', 'ASTROPY_GE_30', 'ASTROPY_GE_31']

ASTROPY_LT_30 = LooseVersion(__version__) < LooseVersion('3.0')
ASTROPY_LT_31 = LooseVersion(__version__) < LooseVersion('3.1')
ASTROPY_GE_30 = not ASTROPY_LT_30
ASTROPY_GE_31 = not ASTROPY_LT_31
