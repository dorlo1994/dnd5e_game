class Skill:
    def __init__(self, name, stat):
        self.name = name
        self.stat = stat

    @property
    def modifier(self):
        return self.stat.modifier
