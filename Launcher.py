import os, sys, re
import subprocess
import utils
from Locator import Locator
from types import *

if not utils.is_posix:
    import win32api

def encapsulate_args_in_quotes(f):
    if re.search(' ', f):
        return '"%s"' % f
    else:
        return f

class Launcher:
    def __init__(self, name, **kwargs):
        self.stderr_to_console = kwargs.get('stderr_to_console', False)
        self.stdout_to_console = kwargs.get('stdout_to_console', False)

        if type(name) is StringType:
            l = Locator(name)
            self.args = [l()]
        elif isinstance(name, Locator):
            self.args = [name()]
        else:
            raise TypeError("Invalid argument for Launcher")

    def __iadd__(self, value):
        if (type(value) is TupleType) or (type(value) is ListType):
            if len(value) == 2:
                self.addArg(value[0], value[1], append = True)
            elif len(value) == 1:
                self.addArg(value[1])
            else:
                raise TypeError ("Adding invalid argument to Launcher")
        else:
            self.addArg(value)

        return self
    
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

    def __str__ (self):
        return ' '.join(self.args)
    
    def __call__(self, **kwargs):
        print_args = kwargs.get('print_args')
        dry_run = kwargs.get('dry_run')
        if dry_run:
            print_args = True
        wait = kwargs.get('wait_for_command_to_complete')
        if print_args:
            print self.args
        if not self.stderr_to_console:
            stderr = subprocess.PIPE
        else:
            stderr = None

        if not self.stdout_to_console:
            stdout = subprocess.PIPE
        else:
            stdout = None

        if dry_run:
            return

        if not os.access(self.args[0], os.X_OK):
            return
        
        if wait:
            subprocess.call(self.args)
        else:
            subprocess.Popen(self.args, stdout = stdout, stderr = stderr)

