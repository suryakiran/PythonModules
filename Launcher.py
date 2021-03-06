import os, sys, re
import subprocess
import PyCommandUtils
from Locator import Locator
from types import *

if not PyCommandUtils.is_posix:
    import win32api

def encapsulate_args_in_quotes(f):
    if re.search(' ', f):
        return '"%s"' % f
    else:
        return f

class Launcher:
    def __init__(self, name, **kwargs):
        self.stderr_to_console = kwargs.get('stderr_to_console', True)
        self.stdout_to_console = kwargs.get('stdout_to_console', True)

        if isinstance(name, str):
            l = Locator(name)
            self.args = [l()]
        elif isinstance(name, Locator):
            self.args = [name()]
        else:
            raise TypeError("Invalid argument for Launcher")

    def __iadd__(self, value):
        if type(value) is ListType:
            for v in value:
                self.addArg(v)
        elif type(value) is TupleType:
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
            for x in value:
                self.args.append(x)

    def addFiles(self, files):
        for f in files:
            if PyCommandUtils.is_posix:
                self.args.append(f)
            else:
                self.args.append(win32api.GetShortPathName(f))

    def __str__ (self):
        return ' '.join(self.args)
    
    def __call__(self, **kwargs):
        print_args = kwargs.get('print_args')
        run_in_dir = kwargs.get('dir')
        dry_run = kwargs.get('dry_run')
        if dry_run:
            print_args = True
        wait = kwargs.get('wait_for_command_to_complete')
        if print_args:
            print (self.args)
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
            if run_in_dir:
                os.chdir(run_in_dir)
            os.execl(self.args[0], *self.args)
        else:
            if run_in_dir:
                subprocess.Popen(self.args, stdout = stdout, stderr = stderr, cwd=run_in_dir)
            else:
                subprocess.Popen(self.args, stdout = stdout, stderr = stderr)

