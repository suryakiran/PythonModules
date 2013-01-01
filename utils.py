import os, sys

is_posix = (os.name == 'posix')

def isExe(path):
    return os.path.isfile(path) and os.access(path, os.X_OK)
