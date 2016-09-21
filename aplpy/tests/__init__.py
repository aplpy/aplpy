from distutils.version import LooseVersion

import matplotlib

MPL_VERSION = LooseVersion(matplotlib.__version__)

ROOT = "http://aplpy.github.io/aplpy-data/1.x/2016-09-21T08:12:02.530/"

if MPL_VERSION >= LooseVersion('1.5.0'):
    baseline_dir = ROOT + '/1.5.x/'
else:
    baseline_dir = ROOT + '/1.4.x/'
