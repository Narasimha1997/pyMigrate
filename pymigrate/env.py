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


def select_dependency(dep, package):

    if package != "":
        answer = input(
                "For module \"{}\", package name is {},".format(dep, package) +
                " would you approve this? (y/Y/yes/YES or n/N/no/NO): "
            )
        answer = str(answer).lower().replace("\n", "")
        if answer == "y" or answer == "yes":
            return package
        if answer == "n" or answer == "no":
            package_name = input(
                "Enter package as <package_name>==<version> or " +
                "<package_name>, for example  \"flask==0.0.1\" : "
            )

            package_name = package_name.strip().replace("\n", "")
            if package_name == "":
                print("Ignoring, using the predicted package name")
                return package
            else:
                return package_name
    else:
        package_name = input(
            "No package was found for \"{}\" on your system, ".format(dep) +
            "provide the package name manually, in format  " +
            "<package_name>==<version> or <package_name>, " +
            "for example => \"flask==0.0.1\": "
        )

        package_name = str(package_name).strip().replace("\n", "")
        if package_name == "":
            print('Ignored module {}'.format(dep))
            return ""
        else:
            print('Registered {} as the package name for {}'.format(
                package_name, dep
            ))
            return package_name


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

    print('\n---------REQUIRES YOUR INPUT, PAY ATTENTION----------------')
    for dep in deps:
        logging.info('Installing ' + str(dep))
        if dep == "":
            continue
        package_name = select_dependency(dep, deps[dep])
        if package_name == "":
            continue
        exec_suffix = ['install', package_name, '--prefix='+virtual_env]
        call([os.path.join(virtual_env, 'bin', 'pip3'), *exec_suffix])
        logging.info('Installed {}'.format(dep))


def get_deps(app):
    deps = DepsHandle(root=app).run_task()
    return deps


def gen_requirements(app, dest):
    deps = get_deps(app)
    dest_path = os.path.join(dest, 'requirements.txt')
    with open(dest_path, 'w') as writer:
        print('\n---------REQUIRES YOUR INPUT, PAY ATTENTION----------------')
        for dep in deps:
            if dep == "":
                continue
            package_name = select_dependency(dep, deps[dep])
            if package_name == "":
                continue
            writer.write("{}\n".format(package_name))
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
