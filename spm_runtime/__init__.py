__all__ = [
    "__version__",
    "__matlab_release__",
    "endpoint",
    "mpython_endpoint",
    "standalone",
]
import sys
from ._version import __version__, __matlab_release__
from ._endpoint import endpoint
from ._standalone import standalone


# Alias used by the spm-python runtime
mpython_endpoint = endpoint


# Standalone entrypoint
if sys.platform == "darwin":
    from matlab_runtime.cli import mwpython2

    def _standalone_entrypoint(args=None):
        if args is None:
            args = sys.argv[1:]
        return mwpython2([
            "-variant", __matlab_release__,
            "-m", "spm_runtime",
            *args
        ])

else:
    _standalone_entrypoint = standalone
