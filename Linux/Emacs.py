import os, sys
from Locator import Locator
from Launcher import Launcher
import subprocess

class EmacsPrivate:
    def __init__(self):
        self.exePath = Locator('emacs')()
        self.emacsClientPath = Locator('emacsclient')()
        homeEnv = os.environ['HOME']
        self._launcher = Launcher(self.exeClientPath)

    def serverList(self):
        return subprocess.check_output([self.exePath, '--serverlist']).split()
        
