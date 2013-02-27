import os

class Environment:
    def __init__(self, envKey):
        self.key = envKey
        env = os.environ.get(envKey)
        if env:
            self.list = env.split(os.pathsep)
        else:
            self.list = []

    def _path_exists(self, d):
        if self.list.count(d):
            return True
        return False
        
    def append(self, val):
        if not self._path_exists(val):
            self.list.append(val)
            self._update()
            
    def append_dir_of(self, val):
        if val:
            d = os.path.dirname(val)
            if not self._path_exists(d):
                self.list.append(val)
                self._update()

    def prepend(self, val):
        if not self._path_exists(val):
            self.list.insert(0, val)
            self._update()

    def prepend_dir_of(self, val):
        if val:
            d = os.path.dirname(val)
            if not self._path_exists(d):
                self.list.insert(0, d)
                self._update()

    def _update(self):
        os.environ[self.key] = os.pathsep.join(self.list)

    def set(self, val):
        self.list = [val]
        self._update()
        
    def __str__(self):
        return ':'.join(self.list)

    def unset(self, val):
        self.list = []
        if os.environ.has_key(self.key):
            os.environ.pop(self.key)
        
