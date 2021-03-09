from venv import EnvBuilder
from .deps_handler import DepsHandle
import shutil
import os
from subprocess import call
import logging
from simple_term_menu import TerminalMenu

extra_options = ["manually specify", "ignore dependency"]


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def create_env(path, options):

    DIR = os.path.join(path)

    logging.info('creating virtual environment')
    builder = EnvBuilder(**options, with_pip=True)
    builder.create(DIR)

    logging.info('Created virtual environment')


def migrate(virt_dir, path):

    logging.info(
        bcolors.OKGREEN + 'Migrating the application...' +
        bcolors.ENDC
    )

    if not os.path.exists(os.path.join(virt_dir, 'app')):
        shutil.copytree(path, os.path.join(virt_dir, 'app'))
        print(bcolors.OKGREEN + 'Migration done.' + bcolors.ENDC)


def ask_package_input(dep):
    pkg_name = input(
                bcolors.BOLD +
                "Specify the package for module {} in the ".format(dep) +
                "format <package_name>==<version> or just <package_name>, " +
                "for example : flask==0.0.1 :\n>> " +
                bcolors.ENDC
            )

    if not pkg_name:
        return ""

    pkg_name = str(pkg_name).strip().replace("\n", "")
    return pkg_name


def select_dependency(dep, packages):
    print()
    if len(packages) == 0:
        print(
            bcolors.WARNING +
            "No package was identified installed on your system for module " +
            "{}, what you want to do??".format(dep) +
            bcolors.ENDC
        )

        menu = TerminalMenu(extra_options)
        selected_idx = menu.show()

        if selected_idx == 0:
            pkg_name = ask_package_input(dep)
            if pkg_name == "":
                print(
                    bcolors.WARNING +
                    "Module {} ignored.".format(dep) +
                    bcolors.ENDC
                )
                return ""
            else:
                print(
                    bcolors.OKGREEN +
                    "Using {} as package for module {}".format(pkg_name, dep) +
                    "." + bcolors.ENDC
                )
                return pkg_name
        else:
            print(
                bcolors.WARNING +
                "Module {} ignored.".format(dep) +
                bcolors.ENDC
            )
            return ""
    else:
        print(
            bcolors.BOLD +
            "Identifed following packages {} ".format(packages) +
            "for module {}, select any one of them or choose ".format(dep) +
            "to ingore or provide your own package name: " +
            bcolors.ENDC
        )

        options = packages
        options.extend(extra_options)
        menu = TerminalMenu(options)
        selected_idx = menu.show()

        if selected_idx == -1 or selected_idx == len(options) - 1:
            print(
                bcolors.WARNING + "Module {} ignored.".format(dep) +
                bcolors.ENDC
            )

            return ""

        elif selected_idx == len(options) - 2:
            pkg_name = ask_package_input(dep)
            if pkg_name == "":
                print(
                    bcolors.WARNING +
                    'Module {} ignored.'.format(dep) +
                    bcolors.ENDC
                )
                return ""
            else:
                print(
                    bcolors.OKGREEN +
                    "Using {} as package for module {}".format(pkg_name, dep) +
                    "." + bcolors.ENDC
                )
                return pkg_name
        else:
            print(
                bcolors.OKGREEN +
                "Using {} as a package for module {}.".format(
                    options[selected_idx],
                    dep
                ) +
                bcolors.ENDC
            )
            return options[selected_idx]


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

    virt_app_req_path = os.path.join(virtual_env, 'app', 'requirements.txt')

    if (not os.path.exists(req_path)) and os.path.exists(virt_app_req_path):
        os.remove(virt_app_req_path)

    all_packages = []

    print('\n---------REQUIRES YOUR INPUT, PAY ATTENTION----------------')
    for dep in deps:
        if dep == "":
            continue
        package_name = select_dependency(dep, deps[dep])
        if package_name == "":
            continue
        all_packages.append(package_name)

    logging.info(
        "Starting to install packages - {}".format(all_packages)
    )

    for package_name in all_packages:
        exec_suffix = ['install', package_name, '--prefix='+virtual_env]
        call([os.path.join(virtual_env, 'bin', 'pip3'), *exec_suffix])
        logging.info('Installed {}'.format(package_name))

        if not os.path.exists(req_path):
            with open(virt_app_req_path, 'a') as writer:
                writer.write("{}\n".format(package_name))

    print(
        bcolors.OKGREEN +
        "Installed all dependencies a selected." +
        bcolors.ENDC
    )


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
    print(
        bcolors.OKGREEN + "Generated requirements.txt at {}".format(dest) +
        bcolors.ENDC
    )
    print(
        bcolors.OKGREEN + 'All done, thanks for using this tool ..' +
        bcolors.ENDC
    )


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
    print(
        bcolors.OKGREEN + 'All done, thanks for using this tool ..' +
        bcolors.ENDC
    )
