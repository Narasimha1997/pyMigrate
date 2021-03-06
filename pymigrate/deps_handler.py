from .parser_import import Parser
from .walk import DirWalk

from multiprocessing.dummy import Pool
import sys
import logging
import pkgutil


class DepsHandle:
    def __init__(self, root='app'):
        self.walker = DirWalk(root=root)
        self.pool = Pool(processes=4)
        self.std_pkg_map = self.prepare_lists()

    def prepare_lists(self):

        std_pkgs = []
        pkgs = pkgutil.iter_modules()
        for pkg in pkgs:
            if not pkg.ispkg:
                std_pkgs.append(pkg.name)
        return std_pkgs

    def check_is_builtin(self, dep_name):
        if dep_name in sys.builtin_module_names:
            return True
        if "_" + dep_name in sys.builtin_module_names:
            return True
        return False

    def check_is_stdlib(self, dep_name):
        if dep_name not in self.std_pkg_map:
            return False
        return True

    def task(self, filename):
        data = open(filename, 'r').readlines()
        parser = Parser()
        return parser.parse(data)

    def run_task(self):
        internal_packages, files = self.walker.traverse()
        lists = self.pool.map(self.task, files)
        identified_packages = []
        # add only external packages to list:
        logging.info("All deps - {}".format(lists))
        for deps in lists:
            for dep in deps:
                should_include = (
                    (dep not in internal_packages) and
                    (not self.check_is_builtin(dep)) and
                    (not self.check_is_stdlib(dep))
                )
                if should_include:
                    identified_packages.append(dep)
        return identified_packages
