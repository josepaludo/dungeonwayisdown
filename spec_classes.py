from time import sleep

from player_class import Player


class Warrior(Player):

    def __init__(self):
        super().__init__()

        self.sym = "W"

        self.var = "qqq"

        self.cards = {"card_name": {"func": self.func, "descr": self.var, "level": "weak"},
                          "aa": {"func": self.func, "descr": self.var, "level": "strong"}}

        self.init_cards()

    def func(self):
        sleep(1)
        for x, y in self.cards.items():
            print(x)
            print(y)
            print(y['level'])
        print(self.strong_cards)
        input()


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

