"""Setuptools build."""
import os.path
import shutil
from setuptools import setup

ROOT = os.path.dirname(__file__)
CTF_PATH = os.path.join(ROOT, "spm_runtime", "_spm", "_spm.ctf")

if not os.path.exists(CTF_PATH):
    import sys
    sys.path.insert(0, ROOT)
    sys.path.insert(0, os.path.join(ROOT, 'scripts'))
    from spm_make_ctf import compile
    try:
        from spm_runtime._version import __spm_sha__ as spm_version
    except Exception:
        spm_version = None
    ctf = compile(spm_version)
    shutil.move(ctf, CTF_PATH)

setup()
