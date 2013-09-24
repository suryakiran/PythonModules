import os, sys
import PyCommandUtils

class SearchInPath:
    def __init__(self, name, *path):
        self.name = name
        self.paths = None
        if not len(path):
            self.paths = os.environ['PATH'].split(os.pathsep)
        else:
            map(lambda x: self.paths.append(x), path)

    def find_if(self, func = os.path.isfile):
        for p in self.paths:
            candidate = os.path.join(p, self.name)
            if func(candidate):
                return candidate
        raise OSError("Can't find file %s" % self.name)

    def find_exe(self):
        return self.find_if(PyCommandUtils.isExe)

if __name__ == '__main__':
    print SearchInPath('emacs').find_exe()
