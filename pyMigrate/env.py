import virtualenv
from pyMigrate.deps_handler import DepsHandler
import shutil
import os
import pip
from subprocess import call



def create_env(path) :

    DIR = os.path.join(path)

    print('creating virtual environment')
    virtualenv.create_environment(DIR)

    print('Created virtual environment')



def migrate(virt_dir, path):

    print('Migrating the application...')

    if not os.path.exists(virt_dir + '/app') : 
        shutil.copytree(path, virt_dir + '/app')
        print('Migration done')

    exec(open(os.path.join(virt_dir, "bin", "activate_this.py")).read())



def install_deps(virtual_env, app):

    print('Scanning for dependencies..')
    deps = DepsHandler(root = app).run_task()

    print('Found dependencies : ', deps)

    print('Installing dependencies .... ')



    for dep in set(deps) : 

        
            print('Installing ' + dep)
            call([virtual_env + '/bin/pip3', 'install', dep , '--prefix='+virtual_env])
            print('Installed ' + dep)
        


#putting it all together : 

def main(virt_dir, app_dir) :

    create_env(virt_dir)

    migrate(virt_dir, app_dir)

    install_deps(virt_dir, app_dir)

    print('All done, thanks for using this tool ..')









