import os, sys, re
from Locator import Locator
import subprocess

class EmacsPrivate:
  def __init__(self):
    self.installDir = Locator('emacs')(key = 'SOFTWARE\Emacs', value = 'install-dir')
    self.exePath = os.path.join(self.installDir, 'bin', 'runemacs.exe')
    self.emacsClientPath = os.path.join(self.installDir, 'bin', 'emacsclient.exe')

  def serverList(self):
    result = []
    child = subprocess.Popen([
        'tasklist', '/v', '/FO', 'LIST', '/FI', 'IMAGENAME eq gvim.exe'
        ], stdout = subprocess.PIPE, shell = True)
    output = filter(None, child.communicate())[0]
    for l in output.split('\n'):
      m = self.serverRegex.match(l)
      if m is not None:
        result.append(m.group(1).strip())
    return result
