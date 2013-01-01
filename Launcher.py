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
    def __init__(self, name, **kwargs):
        self.stderr_to_console = kwargs.get('stderr_to_console', False)
        self.stdout_to_console = kwargs.get('stdout_to_console', False)
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
            
    def __call__(self, **kwargs):
        print_args = kwargs.get('print_args')
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

        if wait:
            subprocess.call(self.args)
        else:
            subprocess.Popen(self.args, stdout = stdout, stderr = stderr)

