"""Setuptools build."""
import os.path
import shutil
from setuptools import setup, Command
import setuptools.command.build

setuptools.command.build.build.sub_commands.append(("build_ctf", None))


ROOT = os.path.dirname(__file__)
CTF_PATH = os.path.join("spm_runtime", "_spm", "_spm.ctf")


class BuildCTF(Command):

    def initialize_options(self):
        self.build_lib = None
        self.editable_mode = False
        self.ctf_src_path = None
        self.ctf_exist = None

    def finalize_options(self):
        self.set_undefined_options("build_py", ("build_lib", "build_lib"))
        self.ctf_src_path = os.path.abspath(CTF_PATH)
        self.ctf_exist = os.path.exists(self.ctf_src_path)

    def run(self):
        if not self.ctf_exist:
            import sys
            sys.path.insert(0, ROOT)
            sys.path.insert(0, os.path.join(ROOT, 'scripts'))
            from spm_make_ctf import compile
            try:
                from spm_runtime._version import __spm_sha__ as spm_version
            except Exception:
                spm_version = None
            ctf = compile(spm_version)
            shutil.move(ctf, os.path.join(self.build_lib, CTF_PATH))

    def get_output_mapping(self):
        """Return dict mapping output file paths to input file paths."""
        return {}

    def get_outputs(self):
        """Return list containing paths to output files."""
        return [os.path.join(self.build_lib, CTF_PATH)]

    def get_source_files(self):
        """Returns list containing paths to input files."""
        return [
            os.path.join("spm_runtime", "_version.py"),
            os.path.join("scripts", "spm_make_ctf.py"),
            os.path.join("scripts", "spm_make_python.m"),
        ]


setup(cmdclass={"build_ctf": BuildCTF})
