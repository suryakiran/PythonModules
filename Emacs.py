import os, sys
from Locator import Locator
from Launcher import Launcher
import commands
import subprocess

class EmacsExpression:
    def __init__(self):
        self.comstr = []
        self.comstr.append('(progn')

    def addStatement(self, stmt):
        self.comstr.append('(%s)' % (stmt))

    def __call__(self):
        self.comstr.append(')')
        return ' '.join(self.comstr)

class Emacs:
    def __init__(self, server_name, **kwargs):
        server_name = server_name.upper()
        self.open_init_file = kwargs.get('open_init_file', False)

        self.files = None
        if not self.open_init_file:
            self.files = kwargs.get('files', None)

        self.emacsExpr = None
        if self.open_init_file:
            self.emacsExpr = EmacsExpression()
            self.emacsExpr.addStatement('skg/open-init-file')

        line = kwargs.get('line', None)
        if line:
            self._gotoLine(line)

        self.exePath = Locator('emacs')()
        self.exeClientPath = Locator('emacsclient')()
        self.homeEnv = os.environ['HOME']
        if self._serverRunning(server_name):
            self._launcher = Launcher(self.exeClientPath)
            self._launcher.addArg('-n')
            self._launcher.addArg('-f', server_name)
        else:
            self._launcher = Launcher(self.exePath)

    def _serverRunning(self, server_name):
        server_list = self._serverList()
        if server_list:
            return bool (server_list.count(server_name))
        else:
            return False

    def _emacsExpr(self):
        if not self.emacsExpr:
            self.emacsExpr = EmacsExpression()
        return self.emacsExpr

    def _gotoLine(self, line):
        self._emacsExpr().addStatement('goto-line %s' % (line))

    def _serverList(self):
        servers_dir = os.path.join(self.homeEnv, '.emacs.d', 'server')
        files = commands.getoutput("ls -l %s | grep '^-' | awk '{print $NF}'" % servers_dir).split('\n')
        return files
        
    def launch(self):
        if self.files:
            self._launcher.addFiles(self.files)
        else:
            self._emacsExpr().addStatement('raise-frame')

        if self.emacsExpr:
            self._launcher.addArg('--eval', self.emacsExpr())

        self._launcher()
