from .parser_import import Parser
from .walk import DirWalk

from multiprocessing.dummy import Pool
import sys
import logging
import pkgutil
import os
import glob


class DepsHandle:
    def __init__(self, root='app'):
        self.walker = DirWalk(root=root)
        self.pool = Pool(processes=4)
        self.std_pkg_map = self.prepare_lists()
        self.package_index = self.preprare_local_package_index()

    def __get_name_version_string(self, metadata_file):

        # print(metadata_file)
        if not os.path.exists(metadata_file):
            return ""

        name_string = ""
        version_string = ""

        name_identifed = False
        version_identified = False

        for line in open(metadata_file):

            if name_identifed and version_identified:
                break

            if line.startswith("Name:"):
                spls = line.split(":")
                if len(spls) > 1:
                    name_string = spls[-1].strip().replace("\n", "")
                name_identifed = True

            if line.startswith("Version"):
                spls = line.split(":")
                if len(spls) > 1:
                    version_string = spls[-1].strip().replace("\n", "")
                version_identified = True

        # form package stirng
        return "{}{}".format(
            "" if name_string == "" else name_string,
            "" if version_string == "" else "=={}".format(version_string)
        )

    def preprare_local_package_index(self):

        package_index = {}

        for package_path in sys.path:
            if not os.path.exists(package_path):
                continue

            # get all file-names with dist-info suffix:
            # if same module exist at multiple locations,
            # they will be appended to the array and user will
            # be asked for selecting the right package.
            search_exp = os.path.join(package_path, "*dist-info*")
            dist_info_paths = glob.glob(search_exp)

            # print(dist_info_paths)

            # for each dist info path, read top-level.txt and build the index
            for dist_info_path in dist_info_paths:
                top_level_file = os.path.join(dist_info_path, "top_level.txt")
                if not os.path.exists(top_level_file):
                    continue

                # read the top-level file and populate the index:
                top_level_entries = open(top_level_file).read().split("\n")
                # get the package name
                metadata_file = os.path.join(dist_info_path, "METADATA")
                package_name = self.__get_name_version_string(metadata_file)

                # print(package_name)

                for top_level_entry in top_level_entries:
                    top_level_entry = top_level_entry.strip()
                    if top_level_entry != "" and \
                            top_level_entry not in package_index:
                        package_index[top_level_entry] = [package_name]
                    elif top_level_entry != "" and \
                            top_level_entry in package_index:
                        package_index[top_level_entry].append(package_name)

        # print(package_index)
        return package_index

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
        identified_packages = {}

        all_deps = set()
        for deps in lists:
            for dep in deps:
                dep = dep.strip()
                if dep == "":
                    continue
                all_deps.add(dep)

        # add only external packages to list:
        logging.info("All deps - {}".format(all_deps))
        for dep in all_deps:
            # dep = dep.strip()
            should_include = (
                (dep not in internal_packages) and
                (not self.check_is_builtin(dep)) and
                (not self.check_is_stdlib(dep))
            )
            if should_include:
                # get the package name and keep it
                if dep in identified_packages:
                    continue

                if dep in self.package_index:
                    identified_packages[dep] = self.package_index[dep]
                else:
                    identified_packages[dep] = []

        return identified_packages
