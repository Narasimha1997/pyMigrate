# pyMigrate
A tool for automatically migrating any python source code to a virtual environment with all 
dependencies automatically identified and installed. You can also use this tool to generate requirements.txt for your python code base, in general, this tool will help you to bring your old/hobby 
python codebase to production/distribution.

## Features:
1. A simple CLI tool.
2. Creates and installs a virtualenv automatically.
3. Identifies the dependencies (external) automatically and populates the `requirements.txt`
4. Installs dependencies in the virtualenv

## How to install:
The package is available on pip. Run:
```
pip3 install pymigrate
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

## Contributing:
Feel free to contribute by raising issues, making PRs or suggesting features.