from distutils.version import LooseVersion
from . import crosshairs

try:
    import galicaster
except:
    print "Error: Galicaster not found"

def init():
    if LooseVersion(galicaster.__version__) <= LooseVersion("2.0.x"):
        crosshairs.init()
    else:
        raise Exception("Plugin version mismatch")
