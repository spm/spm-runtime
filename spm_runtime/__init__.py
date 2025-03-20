__all__ = [
    "__version__",
    "__matlab_release__",
    "endpoint",
]
import matlab_runtime

from ._version import __version__, __matlab_release__
from . import _spm

matlab_runtime.init(__matlab_release__, install_if_missing=True)

_deployed = matlab_runtime.import_deployed(_spm)
endpoint = _deployed.mpython_endpoint
