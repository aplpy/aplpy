# this contains imports plugins that configure py.test for astropy tests.
# by importing them here in conftest.py they are discoverable by py.test
# no matter how it is invoked within the source tree.

from astropy.tests.pytest_plugins import *
from astropy.tests.pytest_plugins import pytest_addoption as astropy_pytest_addoption

# This is to figure out APLpy version, rather than using Astropy's
from . import version

import matplotlib
matplotlib.use('Agg')

try:
    packagename = os.path.basename(os.path.dirname(__file__))
    TESTED_VERSIONS[packagename] = version.version
except NameError:
    pass

# Uncomment the following line to treat all DeprecationWarnings as
# exceptions
enable_deprecations_as_exceptions()

from astropy.tests.helper import pytest


def pytest_addoption(parser):
    parser.addoption('--generate-images-path',
                     help="directory to generate reference images in",
                     action='store')
    return astropy_pytest_addoption(parser)


@pytest.fixture
def generate(request):
    return request.config.getoption("--generate-images-path")

# Add astropy to test header information and remove unused packages.

try:
    PYTEST_HEADER_MODULES['Astropy'] = 'astropy'
    PYTEST_HEADER_MODULES['pyregion'] = 'pyregion'
    PYTEST_HEADER_MODULES['PyAVM'] = 'PyAVM'
    PYTEST_HEADER_MODULES['montage-wrapper'] = 'montage-wrapper'
    del PYTEST_HEADER_MODULES['h5py']
except NameError:
    pass
