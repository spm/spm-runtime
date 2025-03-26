from matlab_runtime.utils import guess_matlab_release

import argparse
import tempfile
import subprocess
import shutil
import os
from datetime import datetime


def guess_version(spm_version=None):

    cwd = os.path.abspath(os.curdir)

    with tempfile.TemporaryDirectory() as tmpdir:

        os.makedirs(os.path.join(tmpdir, "external"), exist_ok=True)
        os.chdir(os.path.join(tmpdir, "external"))

        # Checkout SPM
        shutil.rmtree("spm", ignore_errors=True)
        subprocess.run([
            "git", "clone", "https://github.com/spm/spm",
        ])
        os.chdir("spm")

        if spm_version:
            # Checkout version
            subprocess.run(["git", "fetch", "origin", spm_version])
            subprocess.run(["git", "reset", "--hard", "FETCH_HEAD"])
        else:
            # Guess version
            # -> We use the most recent tag and add ".dev"
            sha = subprocess.run([
                "git", "rev-list", "--tags", "--max-count=1"
            ], capture_output=True).stdout.decode().strip()
            spm_version = subprocess.run([
                "git", "describe", "--tags", sha
            ], capture_output=True).stdout.decode().strip()
            print("Guessed version:", spm_version)

        # Save hash
        sha = subprocess.run([
            "git", "rev-parse", "HEAD"
        ], capture_output=True).stdout.decode().strip()

        # Check if dev
        spm_runtime_version = spm_version
        this_version = spm_version = subprocess.run([
            "git", "describe", "--tags"
        ], capture_output=True).stdout.decode().strip()

        # Check if this is a post-release
        spm_runtime_versions = subprocess.run([
            "git", "tag"
        ], capture_output=True).stdout.decode().strip().split('\n')
        spm_runtime_versions = [x.strip() for x in spm_runtime_versions]

        if "-" in this_version:
            key = ".dev"
        else:
            key = ".post"

        if spm_runtime_version in spm_runtime_versions:
            if any(
                x.startswith(spm_runtime_version + key)
                for x in spm_runtime_versions
            ):
                # there are already post releases -> increment by one
                post = max(
                    int(x[len(spm_runtime_version + key):])
                    for x in spm_runtime_versions
                    if x.startswith(spm_runtime_version + key)
                ) + 1
            else:
                # First post-release
                post = 1
            spm_runtime_version += f"{key}{post}"

        # Guess date
        date = subprocess.run([
            "git", "show", "--no-patch", "--format=%cs"
        ], capture_output=True).stdout.decode().strip()
        date = datetime.strptime("2019-03-02", "%Y-%m-%d").strftime("%d-%b-%Y")

    os.chdir(cwd)
    return {
        "version": spm_runtime_version,
        "spm_version": spm_version,
        "spm_sha": sha,
        "spm_date": date,
    }


def compile(spm_version=None, matlab_release="R2024b", odir="."):

    input_spm_version = spm_version

    versions = guess_version(spm_version)
    spm_runtime_version = versions["version"]
    spm_version = versions["spm_version"]
    date = versions["spm_date"]

    cwd = os.path.abspath(os.curdir)
    odir = os.path.abspath(odir)

    current_release = guess_matlab_release(shutil.which("matlab"))
    if current_release != matlab_release:
        raise RuntimeError(
            "matlab on path is not", matlab_release,
            "but", current_release
        )

    with tempfile.TemporaryDirectory() as tmpdir:

        os.makedirs(os.path.join(tmpdir, "external"), exist_ok=True)
        os.chdir(os.path.join(tmpdir, "external"))

        # Checkout SPM
        shutil.rmtree("spm", ignore_errors=True)
        subprocess.run([
            "git", "clone", "https://github.com/spm/spm",
        ])
        os.chdir("spm")

        if input_spm_version:
            # Checkout version
            subprocess.run(["git", "fetch", "origin", input_spm_version])
            subprocess.run(["git", "reset", "--hard", "FETCH_HEAD"])

        # Set version in content
        SPM_RELEASE = spm_version[:2]
        version_line = f"% Version {spm_version} (SPM{SPM_RELEASE}) {date}"
        with open("tmp", "wb") as f:
            f.write(
                subprocess.run([
                    "sed", f"2s/.*/{version_line}/", "Contents.m",
                ], capture_output=True).stdout
            )
        shutil.move("tmp", "Contents.m")

        os.chdir("..")

        # Checkout MPython
        shutil.rmtree("mpython", ignore_errors=True)
        subprocess.run([
            "git", "clone", "--depth", "1",
            "https://github.com/MPython-Package-Factory/mpython",
        ])

        # Checkout SPM-Runtime
        shutil.rmtree("spm-runtime", ignore_errors=True)
        os.makedirs("spm-runtime/scripts", exist_ok=True)
        shutil.copyfile(
            os.path.join(os.path.dirname(__file__), "spm_make_python.m"),
            "spm-runtime/scripts/spm_make_python.m"
        )

        # Compile
        compile_dir = os.path.abspath('..')
        subprocess.run([
            "matlab", "-batch",
            f"addpath('spm-runtime/scripts');"
            f"spm_make_python('{compile_dir}')"
        ])

        # Copy CTF
        os.makedirs(odir, exist_ok=True)
        ctf_name = f"spm_{matlab_release}_{spm_runtime_version}.ctf"
        shutil.move(
            os.path.join(compile_dir, "spm/_spm/_spm.ctf"),
            os.path.join(odir, ctf_name)
        )

    os.chdir(cwd)
    return os.path.join(odir, ctf_name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--spm-version", default=None)
    parser.add_argument("-r", "--matlab-runtime", default="R2024b")
    parser.add_argument("-o", "--output", default=".")
    p = parser.parse_args()
    compile(p.spm_version, p.matlab_runtime, p.output)


if __name__ == "__main__":
    main()
