from time import sleep

from player_class import Player

#self.cards = {"card_name": {"func": self.func, "descr": self.var, "level": "weak"},


class Warrior(Player):

    def __init__(self):
        super().__init__()

        self.sym = "W"

        self.wek_a = "Swings your axe in a direction, hiting a single enemy and dealing damage."
        self.wek_j = "Gains an extra move."
        self.mid_p = "Tries to taunt each oponent until your next turn."
        self.mid_m = "Ignores some damage until your next turn."
        self.str_t = "Taunts each oponent."
        self.str_m = "Ignores all damage until end of turn."

        self.cards = {"Axe Swing": {"func": self.wek_as_f, "descr": self.wek_a, "level": "weak"},
                      "Jump": {"func": self.wek_j_f, "descr": self.wek_j, "level": "weak"},
                      "Mitigate": {"func": self.mid_m_f, "descr": self.mid_m, "level": "medium"},
                      "Provoke": {"func": self.mid_p_f, "descr": self.mid_p, "level": "medium"},
                      "Taunt": {"func": self.str_t_f, "descr": self.str_t, "level": "strong"},
                      "Ignore Pain": {"func": self.str_m_f, "descr": self.str_m, "level": "strong"}}

        self.init_cards()


    def wek_as_f(self):

        for x in self.get_urdl_coords(self.y, self.x):
            print(x)
        for y in self.get_urdl_coords_range(self.y, self.x, 3):
            print(y)
        input()


    def wek_j_f(self):
        pass


    def mid_p_f(self):
        pass


    def mid_m_f(self):
        pass


    def str_t_f(self):
        pass


    def str_m_f(self):
        pass


class Priest(Player):

    def __init__(self):
        super().__init__()

        self.sym = "P"

        self.cards = {"card_name": {"func": self.func, "descr": self.var, "level": "weak"}}


class Druid(Player):

    def __init__(self):
        super().__init__()

        self.sym = "D"


        self.cards = {"card_name": {"func": self.func, "descr": self.var, "level": "weak"}}


class Wizard(Player):

    def __init__(self):
        super().__init__()

        self.sym = "Z"

        self.cards = {"card_name": {"func": self.func, "descr": self.var, "level": "weak"}}


class Thief(Player):

    def __init__(self):
        super().__init__()

        self.sym = "T"

        self.cards = {"card_name": {"func": self.func, "descr": self.var, "level": "weak"}}

