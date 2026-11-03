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
    from matlab_runtime.cli import mpython

    def _standalone_entrypoint(args=None):
        if args is None:
            args = sys.argv[1:]
            
        if sys.stdin is not None and sys.stdin.isatty():
            from matlab_runtime import install
            from matlab_runtime.utils import deployed_ctf
            try:
                install(
                    __matlab_release__, 
                    if_missing="mwpython",
                    default_scope="user", 
                    ctf=deployed_ctf("spm_runtime._spm")
                )
            except (Exception, KeyboardInterrupt) as e:
                print(f"Could not install the MATLAB Runtime: {e}", file=sys.stderr)
                
        return mpython([
            "-variant", __matlab_release__, 
            "-m", "spm_runtime", 
            *args
        ])

else:
    _standalone_entrypoint = standalone
