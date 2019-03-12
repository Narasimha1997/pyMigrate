# pyMigrate
A tool that automates the transformation of normal python projects to virtual environments. In simple words, the tool creates a virtual environment and automatically installs all the dependencies used in your project by identifying them and migrates the project to the newly created virtual environment.

## Set-up : 
This package will be released on pip soon, until then, you can copy pyMigrate to python package path and use pyMigrate.py to perform migration.

## Usage: 

For help : 
```
pyMigrate.py help
```

```
pyMigrate.py app_root_directory virtual_env_directory
```

<p><strong>app_root_directory</strong> : The root directory of your project</p>
<p><strong>virtual_env_directory</strong> : The place where virtualenv should be created</p>

**This project is only for python3 environments**
