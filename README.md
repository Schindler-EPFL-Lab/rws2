# ABB Robot Web Server 2

[![Build Status](https://dev.azure.com/devsdb/CRD-NT_ARCO/_apis/build/status/SchindlerReGIS.rws2?branchName=main)](https://dev.azure.com/devsdb/CRD-NT_ARCO/_build/latest?definitionId=1209&branchName=main)

This package provides code to interact with [ABB robot web service](https://developercenter.robotstudio.com/api/RWS?urls.primaryName=Introduction).
Tested and developed for version `3HAC073675-001 Revision:D` with an ABB GoFa robot.

Code updated from [ABB Robot Web Service](https://github.com/prinsWindy/ABB-Robot-Machine-Vision/tree/master/RobotWebServices).

## License

This work is under the GNU AFFERO GENERAL PUBLIC LICENSE.
If you would like to use this work under another LICENSE than this one, please contact us directly.

## Build and Test

1. Install [flit](https://github.com/pypa/flit) with `pip install flit`.
We use flit to package and install this repository.
2. Clone/fork the repo from Github.
3. Run `pip install -e .` in the root folder to install rws2 in editable mode (`pip install .` is enough if you do not plan to contribute).

The library should then be installed and you should be able to call it in python with `import rws2`.

## How to use

The library is made of two classes:

* `RWS` in `RWS2.py` implements the Robot Web Server protocol as specified by ABB.
* `RWSWrapper` in `RWS_wrapper.py` implements higher level helper functions to control an ABB robot.

Documentation is in the code.

## Contribute

PR request on GitHub are welcome.
We use [black](https://github.com/psf/black) for code formatting and [flake8](https://github.com/pycqa/flake8) for linting.
Code that do not follow black formatting and follow flake8 linting will be rejected by the pipeline.

A standard git commit message consists of three parts, in order: a summary line, an optional bod.
The parts are separated by a single empty line.
The summary line is included in the short logs (git log --oneline, gitweb, Azure DevOps, email subject) and therefore should provide a short yet accurate description of the change.
The summary line is a short description of the most important changes. The summary line must not exceed 50 characters, and must not be wrapped. The summary should be in the imperative tense.
The body lines must not exceed 72 characters and can describe in more details what the commit does.
