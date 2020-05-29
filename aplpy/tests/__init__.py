import matplotlib

MPL_VERSION = matplotlib.__version__

ROOT = "https://aplpy.github.io/aplpy-data/2.x/2018-10-28T17:43:23.106"

# The developer versions of the form 3.2.x+... contain changes that will only
# be included in the 3.3.x release, so we update this here.
if MPL_VERSION[:3] == '3.2' and '+' in MPL_VERSION:
    MPL_VERSION = '3.3'

baseline_dir = ROOT + '/' + MPL_VERSION[:3] + '.x/'
