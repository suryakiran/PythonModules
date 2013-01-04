import os, sys
from Locator import Locator
from Launcher import Launcher

class Gdb:
    def __init__(self, **kwargs):
        self.debug = kwargs.get('debug', True)
        self.exe_file = kwargs.get('exe_file')
        self.dry_run = kwargs.get('dry_run')

        if self.debug:
            self.debugger = Locator('cgdb')()
            self.debugger_is_cgdb = False
            self.init_file = kwargs.get('init_file')

            if not self.debugger:
                self.debugger = Locator('gdb')()
            else:
                self.debugger_is_cgdb = True

    def _debug_app(self, **kwargs):
        launcher = Launcher(self.debugger)
        launcher.addArg(self.exe_file)
        if self.debugger_is_cgdb:
            launcher.addArg('--')

        if self.init_file and os.access(self.init_file, os.R_OK):
            launcher.addArg('-x', self.init_file)
            
        if kwargs is not None:
            launcher.addArg('--args', self.exe_file)
        return launcher
    
    def __call__(self, **kwargs):
        launcher = None
        if self.debug and self.debugger:
            launcher = self._debug_app(**kwargs)
        else:
            launcher = Launcher(self.exe_file, stdout_to_console = True, stderr_to_console = True)
            
        if kwargs is not None:
            for key in kwargs:
                launcher.addArg('--%s' % key, '%s' % kwargs[key], append=True)

        launcher(dry_run = self.dry_run, wait_for_command_to_complete = True)
        
