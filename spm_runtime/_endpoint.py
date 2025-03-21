
class _Endpoint:
    # Lazy mpython endpoint.
    # This is so the matlab runtime is only intiialized if the endpoint
    # is used. This allows us to implement a `spm_standalone` entrypoint
    # that calls mwpython2 if needed.

    def __init__(self):
        self._deployed = None

    def _init_endpoint(self):
        import matlab_runtime
        from ._version import __matlab_release__
        from . import _spm
        matlab_runtime.init(__matlab_release__, install_if_missing=True)
        self._deployed = matlab_runtime.import_deployed(_spm)

    def __call__(self, *args, **kwargs):
        if self._deployed is None:
            self._init_endpoint()
        return self._deployed.mpython_endpoint(*args, **kwargs)


endpoint = _Endpoint()
