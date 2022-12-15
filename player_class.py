from living_classes import Living

class Player:

    def __init__(self):
        super().__init__()

        self.input_list = ["help", "log", "cards", "status", "weapons", "icons", "more help", "move"]
        self.inputs = {"move": self.move}

    def move(self):
        print("this is move")

class Warrior(Player):

    def __init__(self):
        super().__init__()

        self.sym = "W"
        self.input_list += ["aaaaaaaaaaaaaaaaaaaaaaa"]

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
