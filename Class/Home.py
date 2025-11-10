from system.lib.minescript import execute


class Home:
    def __init__(self, name: str):
        self.name = name

    def tp(self):
        execute("home " + self.name)
