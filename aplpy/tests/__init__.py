from distutils.version import LooseVersion

import matplotlib

MPL_VERSION = LooseVersion(matplotlib.__version__)

ROOT = "http://aplpy.github.io/aplpy-data/1.x/2017-05-08T14:01:14.323/"

if MPL_VERSION >= LooseVersion('1.5.0'):
    baseline_dir = ROOT + '/1.5.x/'
else:
    baseline_dir = ROOT + '/1.4.x/'
