import os, sys, re
import subprocess
import utils

if not utils.is_posix:
    import win32api

def encapsulate_args_in_quotes(f):
    if re.search(' ', f):
        return '"%s"' % f
    else:
        return f

class Launcher:
    def __init__(self, name):
        self.args = [name]

    def addArg(self, key, *value, **kwargs):
        append = kwargs.get('append', None)
        if len(value) and append:
            self.args.append(key + '=' + ','.join(map(str, value)))
        else:
            self.args.append(key)
            map(lambda x: self.args.append(x), value)

    def addFiles(self, files):
        for f in files:
            if utils.is_posix:
                self.args.append(f)
            else:
                self.args.append(win32api.GetShortPathName(f))
            
    def __call__(self):
        subprocess.Popen(self.args)
