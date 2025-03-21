import sys
from ._endpoint import endpoint


def standalone(args=None):
    if args is None:
        args = sys.argv[1:]
    try:
        endpoint("spm_standalone", *args, nargout=0)
        # FIXME: This is maybe not the most robust condition
        while endpoint("eval", "numel(allchild(0))", nargout=1):
            continue
    except KeyboardInterrupt:
        return 0
    except Exception as e:
        print(e, file=sys.stderr)
        return 1
