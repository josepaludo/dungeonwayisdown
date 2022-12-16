from time import sleep

from player_class import Player


class Warrior(Player):

    def __init__(self):
        super().__init__()

        self.sym = "W"

        self.var = "qqq"

        self.all_cards = {"card_name": {"func": self.func, "descr": self.var},
                          "aa": {"func": self.func, "descr": self.var}}


    def func(self):
        sleep(1)
        print("AAAAAA")
        sleep(1)


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

