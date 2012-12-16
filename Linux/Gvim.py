import os, sys
from Locator import Locator
from Launcher import Launcher
import subprocess

class GvimPrivate:
    def __init__(self):
        self.exePath = Locator('gvim')()
        homeEnv = os.environ['HOME']
        self.gvimRcFile = os.path.join(homeEnv, '.gvimrc')
        self.gvimRcLocalFile = os.path.join(homeEnv, '.gvimrc-local')
        self._launcher = Launcher(self.exePath)

    def serverList(self):
        return subprocess.check_output([self.exePath, '--serverlist']).split()
        
