import os


class DirWalk:

    def __init__(self, root='app'):
        self.root = root

    # returns a list of flienames
    def walk(self):
        project_files = []
        internal_packages = []

        for dir_, subdir_, files in os.walk(self.root):
            internal_packages += subdir_
            for fname in files:
                if fname.endswith(".py"):
                    project_files.append(dir_ + '/' + fname)
                    internal_packages.append(fname[:-3])
        return (internal_packages, project_files)

    def traverse(self):
        packages, files = self.walk()
        return set(packages), set(files)
