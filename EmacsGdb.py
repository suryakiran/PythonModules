import os, sys
from Emacs import Emacs
from Emacs import EmacsExpression
from Launcher import Launcher
from Locator import Locator

class EmacsGdb (Emacs):
    def __init__(self, server_name, **kwargs):
        super(EmacsGdb, self).__init__(server_name, **kwargs)
        self.exeToDebug = kwargs.get('exe_to_debug')
        self.gdb = Locator('gdb').locate()
        self.gdbCl = Launcher(self.gdb)
        self.gdbCl.addArg('-i', 'mi', append = True)
        self.gdbCl.addArg(self.exeToDebug)
        self.firstArg = True

    def addArg(self, key, *value, **kwargs):
        self.gdbCl.addArg (key, *value, **kwargs)
        
    def launch(self, **kwargs):
        self._emacsExpr().addStatement('gdb "%s"' % (self.gdbCl))
        self._emacsExpr().addStatement('gdb-many-windows t')
        super(EmacsGdb, self).launch(**kwargs)

    def __call__(self, **kwargs):
        dry_run = kwargs.get('dry_run')
        self.launch(dry_run = dry_run)
