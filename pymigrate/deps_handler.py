from .parser_import import Parser
from .walk import DirWalk
from multiprocessing.dummy import Pool


class DepsHandle:
    def __init__(self, root='app'):
        self.walker = DirWalk(root=root)
        self.pool = Pool(processes=4)

    def task(self, filename):
        data = open(filename, 'r').readlines()
        parser = Parser()
        return parser.parse(data)

    def run_task(self):
        internal_packages, files = self.walker.traverse()
        lists = self.pool.map(self.task, files)
        identified_packages = []
        # add only external packages to list:
        for deps in lists:
            for dep in deps:
                if dep not in internal_packages:
                    identified_packages.append(dep)
        return identified_packages
