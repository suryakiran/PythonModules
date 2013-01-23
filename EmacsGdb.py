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
        self._emacsExpr().addStatement('gdb "%s"' % (self.gdbCl))
        self._emacsExpr().addStatement('gdb-many-windows t')
        self.launch(dry_run = False)

    
if __name__ == '__main__':
    e = EmacsGdb('TestGdb',
                 exe_to_debug = '/home/surya/Projects/BuildArea/CodeSamples/StageArea/Debug/pythonify/bin/debug-variant'
                 )
