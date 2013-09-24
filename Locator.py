import os, sys
import PyCommandUtils
from SearchInPath import SearchInPath

if not PyCommandUtils.is_posix:
    import _winreg as reg
    import win32api as win32

class Locator:
    def __init__(self, name):
        if not PyCommandUtils.is_posix:
            self.exeName = os.path.basename(name) + '.exe'
        else:
            self.exeName = name

    def locate (self, **kwargs):
        exe = None
        if PyCommandUtils.is_posix:
            try:
                exe = SearchInPath(self.exeName).find_exe()
            except OSError:
                pass
        else:
            reg_family = kwargs.get('family', None)
            reg_key = kwargs.get('key', None)
            reg_value = kwargs.get('value', None)
            reg_handle = None
            if reg_family is None:
                reg_family = reg.HKEY_LOCAL_MACHINE
            if reg_key is not None:
                try:
                    reg_handle = reg.OpenKey(reg_family, reg_key)
                    exe, _ = reg.QueryValueEx(reg_handle, reg_value)
                except WindowsError:
                    return exe
                
                
        return exe

    def __call__(self, **kwargs):
        return self.locate(**kwargs)
