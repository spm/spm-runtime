import sys
from ._endpoint import endpoint


def standalone(args=None):
    if args is None:
        args = sys.argv[1:]
    # endpoint("spm_standalone", *args, nargout=0)
    try:
        endpoint("spm_standalone", *args, nargout=0)
        return 0
    except Exception as e:
        print(e, file=sys.stderr)
        return 1


if __name__ == "__main__":
    standalone()
