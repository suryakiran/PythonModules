import os, sys, re
from Locator import Locator
import subprocess

class GvimPrivate:
  def __init__(self):
    self.exePath = Locator('gvim')(key = 'SOFTWARE\Vim\Gvim', value = 'path')
    self.gvimRcFile = os.path.normpath(os.path.join(self.exePath, '..', '..', '_gvimrc'))
    self.gvimRcLocalFile = os.path.normpath(os.path.join(self.exePath, '..', '..', 'gvimrc-local'))
    self.serverRegex = re.compile('^Window Title: \[[^\]]*\] - (.*)')

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
    
    
