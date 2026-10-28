
class _Endpoint:
    # Lazy mpython endpoint.
    # This is so the matlab runtime is only intiialized if the endpoint
    # is used. This allows us to implement a `spm_standalone` entrypoint
    # that calls mwpython2 if needed.

    def __init__(self):
        self._deployed = None

    def _init_endpoint(self):
        from matlab_runtime import import_deployed
        from . import _spm
        self._deployed = import_deployed(
            _spm,
            install_if_missing=True,
            only_needed_products=True,
        )

    def __call__(self, *args, **kwargs):
        if self._deployed is None:
            self._init_endpoint()
        return self._deployed.mpython_endpoint(*args, **kwargs)


endpoint = _Endpoint()
