import os, sys
from Locator import Locator
from Launcher import Launcher
import commands
import subprocess

class EmacsPrivate:
    def __init__(self):
        self.exePath = Locator('emacs')()
        self.exeClientPath = Locator('emacsclient')()
        self.homeEnv = os.environ['HOME']
        self._launcher = Launcher(self.exeClientPath)

    def serverList(self):
        servers_dir = os.path.join(self.homeEnv, '.emacs.d', 'server')
        files = commands.getoutput("ls -l %s | grep '^-' | awk '{print $NF}'" % servers_dir).split('\n')
        
    def launcher(self):
        return self._launcher
