# pyMigrate
A tool for automatically migrating any python source code to a virtual environment with all 
dependencies automatically identified and installed. You can also use this tool to generate requirements.txt for your python code base, in general, this tool will help you to bring your old/hobby 
python codebase to production/distribution.

## Features:
1. A simple CLI tool.
2. Creates and installs a virtual environment automatically.
3. Identifies the dependencies (external) automatically and populates the `requirements.txt`
4. Installs dependencies in the virtual environment.
5. Multiple configuration parameters.

## Requirements:
1. pip
2. Python 3.x.x
3. venv

**Note:** : You many need to install `python3-venv` via `apt` on debian systems.

## How to install:
The package is available on pip. Run:
```
pip3 install py-migrate
```
Or you can clone the repository and install manually:
```
git clone https://github.com/Narasimha1997/pyMigrate.git
cd pyMigrate && python3 setup.py install
```

## How to run this tool:
Once installed, the tool will be available through command `pymigrate`. Say you have a codebase at `/path/to/source` and you want to generate the virtualenv with all the dependencies and source code installed at `/path/to/target`, then:

```
pymigrate /path/to/source /path/to/target
```
command will generate the virtualenv for you. The target must be an absloute path.

#### Generating requirements.txt alone, without setting up virtualenv:
You can set `--requirements` to generate `requirements.txt` alone, this will not set-up the virtualenv. Say you have to generate `requirements.txt` at `/path/to/output`, then:

```
pymigrate /path/to/source /path/to/target --requirements
```

## Configuration options:
You can change the default behaviour of the generated virtual environment by setting some of the coniguration options provided. You can run the following command to learn more about these parameters:
```
pymigrate --help
```
Which outputs:
```
usage: pymigrate [-h] [--requirements] [--syspkgs] [--symlink] source target

A tool for automatically migrating any python source code to a virtual
environment with all dependencies automatically identified and installed. You
can also use this tool to generate requirements.txt for your python code base,
in general, this tool will help you to bring your old/hobby python codebase to
production/distribution.

positional arguments:
  source          Path to source directory where you have the codebase to
                  transform
  target          Path to the destination where you need to generate a
                  virtual-environment or requirements.txt

optional arguments:
  -h, --help      show this help message and exit
  --requirements  This flag tells the tool to generate requirements.txt
  --syspkgs       Set this flag, if you want to use system site-packages In
                  other words, you will re-use the packages available on the
                  system instead of downloading them locally in the
                  virtualenv.
  --symlink       Symlinks the python interpreter available on the system
                  rather than installing a new one.
```
## Contributing:
Feel free to contribute by raising issues, making PRs or suggesting features.
