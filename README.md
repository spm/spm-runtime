# spm-runtime
Compiled SPM package that can be called from Python

## Installation

```shell
$ pip install git+https://github.com/balbasty/spm-runtime
```

Once deployed, installation will be possible through:

```shell
$ pip install spm-runtime
$ pip install spm-runtime==25.01
$ pip install spm-runtime-R2024b
$ pip install spm-runtime-R2024b==25.01
```

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
