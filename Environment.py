import os

class Environment:
    def __init__(self, envKey):
        self.key = envKey
        env = os.environ.get(envKey)
        if env:
            self.list = env.split(os.pathsep)
        else:
            self.list = []

    def append(self, val):
        self.list.append(val)
        self._update()

    def prepend(self, val):
        self.list.insert(0, val)
        self._update()

    def _update(self):
        os.environ[self.key] = os.pathsep.join(self.list)

    def set(self, val):
        self.list = [val]
        self._update()

    def unset(self, val):
        self.list = []
        if os.environ.has_key(self.key):
            os.environ.pop(self.key)
        
