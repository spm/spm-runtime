import argparse
import toml
from matlab_runtime.utils import SUPPORTED_PYTHON_VERSIONS


def _make_parser():
    p = argparse.ArgumentParser()
    p.add_argument("--matlab-version", required=True)
    p.add_argument("--spm-version")
    p.add_argument("--spm-sha")
    p.add_argument("--main-package", action='store_true')
    return p


def _requires_python(python_versions):
    python2_versions = [v for v in python_versions if v[0] == '2']
    python3_versions = [v for v in python_versions if v[0] == '3']
    if python2_versions:
        python_versions = ">=" + python2_versions[0]
        if python3_versions:
            # upper bound
            last_version = python3_versions[-1]
            maj, min = map(int, last_version.split('.'))
            python_versions += f",<{maj}.{min+1}"
            # skip python3 below lower bound
            first_version = python3_versions[0]
            maj, min = map(int, first_version.split('.'))
            for i in range(0, min):
                python_versions += f",!={maj}.{i}"
    elif len(python3_versions) == 1:
        python_versions = "==" + python3_versions[0]
    else:
        # lower bound
        python_versions = ">=" + python3_versions[0]
        # upper bound
        last_version = python3_versions[-1]
        maj, min = map(int, last_version.split('.'))
        python_versions += f",<{maj}.{min+1}"

    return python_versions


def _main():
    p = _make_parser().parse_args()
    R = p.matlab_version
    V = p.spm_version
    S = p.spm_sha

    python_versions = list(SUPPORTED_PYTHON_VERSIONS[R])

    # Fix pyproject.toml
    pyproject = toml.load("pyproject.toml")
    project = pyproject.get("project")
    if p.main_package:
        project['name'] = "spm-runtime"
    else:
        project['name'] = f"spm-runtime-{R}"
    if V:
        project['version'] = V
    project['requires-python'] = _requires_python(python_versions)
    project['classifiers'] = [
        classifier for classifier in project['classifiers']
        if not classifier.startswith("Programming Language :: Python")
    ]
    project['classifiers'] += [
        "Programming Language :: Python :: " + python_version
        for python_version in python_versions
    ]
    with open("pyproject.toml", "w") as f:
        toml.dump(pyproject, f)

    # Fix _version.py
    with open("spm_runtime/_version.py", "rt") as f:
        input_metadata = {}
        for line in f:
            if not line.strip():
                continue
            key, val = line.split("=")
            key, val = key.strip(), val.strip()
            input_metadata[key] = val

    with open("spm_runtime/_version.py", "wt") as f:
        V = V or input_metadata["__version__"]
        S = S or input_metadata.get("__spm_sha__", None)
        lines = [
            f'__version__ = "{V}"',
            f'__matlab_release__ = "{R}"',
        ]
        if S:
            lines += [f'__spm_sha__ = "{S}"']
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    _main()
