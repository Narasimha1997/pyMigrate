from venv import EnvBuilder
from .deps_handler import DepsHandle
import shutil
import os
from subprocess import call
import logging


def create_env(path, options):

    DIR = os.path.join(path)

    logging.info('creating virtual environment')
    builder = EnvBuilder(**options, with_pip=True)
    builder.create(DIR)

    logging.info('Created virtual environment')


def migrate(virt_dir, path):

    logging.info('Migrating the application...')

    if not os.path.exists(os.path.join(virt_dir, 'app')):
        shutil.copytree(path, os.path.join(virt_dir, 'app'))
        logging.info('Migration done')


def install_deps(virtual_env, app):
    logging.info('Scanning for dependencies..')
    deps = []

    # if requirements.txt exists, no need to identify dependencies
    req_path = os.path.join(app, "requirements.txt")
    if os.path.exists(req_path):
        req_data = open(req_path, 'r').read()
        deps = req_data.split("\n")
        logging.info("Found requirements.txt in the local project")
        logging.info(
            "Found following packages in requirements.txt - {}"
            .format(deps)
        )
    else:
        deps = DepsHandle(root=app).run_task()

    logging.info('Found dependencies : {}'.format(deps))
    logging.info('Installing dependencies .... ')

    for dep in set(deps):
        logging.info('Installing ' + str(dep))
        exec_suffix = ['install', dep, '--prefix='+virtual_env]
        call([os.path.join(virtual_env, 'bin/pip3'), *exec_suffix])
        logging.info('Installed {}'.format(dep))


def get_deps(app):
    deps = DepsHandle(root=app).run_task()
    return set(deps)


def gen_requirements(app, dest):
    deps = get_deps(app)
    dest_path = os.path.join(dest, 'requirements.txt')
    with open(dest_path, 'w') as writer:
        for dep in deps:
            writer.write("{}\n".format(dep))
    logging.info("Generated requirements.txt at {}".format(dest))


def check_path_exist(path, check_abs=False):
    path_exist = os.path.exists(path)
    if path_exist and check_abs and not os.path.isabs(path):
        return False
    return path_exist


# putting it all together :
def gen_virt_env(virt_dir, app_dir, options):
    create_env(virt_dir, options)
    migrate(virt_dir, app_dir)
    install_deps(virt_dir, app_dir)
    logging.info('All done, thanks for using this tool ..')
