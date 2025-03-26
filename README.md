# spm-runtime

Compiled [Statistical Parametric Mapping (SPM)](https://www.fil.ion.ucl.ac.uk/spm/)
package that can be called from Python.

This package contains the compiled SPM runtime used by
[`spm-python`](https://github.com/spm/spm-python).

## Installation

```shell
# Version built against the latest available MATLAB runtime
$ pip install spm-runtime
$ pip install spm-runtime==25.01
# Version built against a specific version of the MATLAB runtime
$ pip install spm-runtime-R2024b
$ pip install spm-runtime-R2024b==25.01
```

> [!WARNING]
> The repository does not contain the compiled CTF file, but wheels
> released on pypi or as part of our GitHub releases do.
> It is not advised to install `spm-runtime` directly from the
> repository, as it assumes that the matlab compiler is available.
> Installation from our releases wheels and distributions is preferred.

## Supported Python versions

Different versions of the MATLAB runtime are compatible with a [different
range of python versions](https://uk.mathworks.com/support/requirements/python-compatibility.html).
To use the runtime with a python version that is not supported by the latest
MATLAB runtime, you can choose to install a package specifically compiled
against another MATLAB runtime. The python versions supported by each
MATLAB runtime is provided in the table below:

| MATLAB | Python     |
| ------ | ---------- |
| R2024b | 3.9 - 3.12 |
| R2024a | 3.9 - 3.11 |
| R2023b | 3.9 - 3.11 |
| R2023a | 3.8 - 3.10 |
| R2022b | 3.8 - 3.10 |
| R2022a | 3.8 - 3.9  |
| R2021b | 3.7 - 3.9  |
| R2021a | 3.7 - 3.8  |
| R2020b | 3.6 - 3.8  |
| R2020a | 3.6 - 3.7  |

## SPM standalone

On installation, `spm-runtime` exposes the SPM standalone, which can
be executed in a terminal by calling `spm`.

```text
$ spm --help

SPM - Statistical Parametric Mapping
https://www.fil.ion.ucl.ac.uk/spm/

Usage: spm [ fmri | eeg | pet ]
       spm COMMAND [arg...]
       spm [ -h | --help | -v | --version ]

Commands:
    batch          Run a batch job
    script         Execute a script
    function       Execute a function
    eval           Evaluate a MATLAB expression
    [NODE]         Run a specified batch node

Options:
    -h, --help     Print usage statement
    -v, --version  Print version information

Run 'spm [NODE] help' for more information on a command.
```

## Python runtime

This package ships a compiled version of SPM that can be called from
Python:

```python
import spm_runtime

spm_runtime.endpoint("spm_standalone", nargout=0)
```

All MATLAB functions from the SPM package can be called.
However, the inputs and outputs of these bindings are not very user-friendly.
For pythonic bindings, use the
[`spm-python`](https://github.com/spm/spm-python) package (which uses
`spm-runtime` under the hood).
