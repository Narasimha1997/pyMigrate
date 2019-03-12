#!/usr/bin/python3

from pyMigrate import env
import sys

#arguments : 

#structure : 

#python3 run.py app_root_path virtual_env_path

def main():

    if len(sys.argv) == 2 and sys.argv[1] == 'help' : 

        print('pyMigrate is a tool for automating the transformation of existing python projects to virtual environments')
        print('It uses virtualenv and to create a virtual environment and automatically identifies and installs dependencies.')
        print('Format : pyMigrate app_root virtual_env_path')

        return

    if len(sys.argv) < 3 :

        print('Arguments not sufficient')
        return
    
    APP = sys.argv[1]
    ENV_PATH = sys.argv[2]

    env.main(ENV_PATH, APP)

main()


