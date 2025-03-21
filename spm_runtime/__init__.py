__all__ = [
    "__version__",
    "__matlab_release__",
    "endpoint",
    "standalone",
]
import sys
from ._version import __version__, __matlab_release__
from ._endpoint import endpoint

if sys.platform == "darwin":
    from matlab_runtime.cli import mwpython2

    def standalone(args=None):
        if args is None:
            args = sys.argv[1:]
        return mwpython2(["-m", "spm_runtime._standalone", *args])

else:
    from ._standalone import standalone
