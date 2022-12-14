from living_classes import Living

class Player():

    def __init__(self):
        super().__init__()


class Warrior(Player):

    def __init__(self):
        super().__init__()

        self.sym = "W"

class Priest(Player):

    def __init__(self):
        super().__init__()

        self.sym = "P"


class Druid(Player):

    def __init__(self):
        super().__init__()

        self.sym = "D"


class Wizard(Player):

    def __init__(self):
        super().__init__()

        self.sym = "Z"


class Thief(Player):

    def __init__(self):
        super().__init__()

        self.sym = "T"
