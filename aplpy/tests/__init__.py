from distutils.version import LooseVersion

import matplotlib

MPL_VERSION = LooseVersion(matplotlib.__version__)

ROOT = "http://aplpy.github.io/aplpy-data/2.x/2017-07-29T21:57:08.143"

if MPL_VERSION >= LooseVersion('2.0.0'):
    baseline_dir = ROOT + '/2.0.x/'
elif MPL_VERSION >= LooseVersion('1.5.0'):
    baseline_dir = ROOT + '/1.5.x/'
else:
    baseline_dir = ROOT + '/1.4.x/'
