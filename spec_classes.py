from player_class import Player

# self.cards = {"card_name": {"func": self.func, "descr": self.var, "level": "weak"},


class Warrior(Player):

    def __init__(self):
        super().__init__()

        self.sym = "W"
        self.name = "Warrior"
        self.weapon_sym = "x"

        wek_a = "Swings your axe in a direction, hiting a single enemy."
        mid_p = "Tries to taunt each oponent until your next turn."
        mid_m = "Ignores some damage until your next turn."
        str_t = "Taunts each oponent."
        str_m = "Ignores all damage until end of turn."

        self.cards["Axe Swing"] = {"func": self.swing_axe, "descr": wek_a, "level": "weak"}
        self.cards["Mitigate"] = {"func": self.mid_m_f, "descr": mid_m, "level": "medium"}
        self.cards["Provoke"] = {"func": self.mid_p_f, "descr": mid_p, "level": "medium"}
        self.cards["Taunt"] = {"func": self.str_t_f, "descr": str_t, "level": "strong"}
        self.cards["Ignore Pain"] = {"func": self.str_m_f, "descr": str_m, "level": "strong"}

        self.init_cards()

    def swing_axe(self):

        damage = 5

        valid_input = self.prompt_for_direction()

        if not valid_input:
            return

        target = self.get_urdl_coords(self.y, self.x, 1)[valid_input-1][0]

        for enemy in self.enemies:

            if ((enemy.y, enemy.x) == (target[0], target[1])) and not enemy.dead:
                enemy.health -= damage

                message = f"{self.name} dealt {damage} damage to {enemy.name} with his axe."
                self.board.add_log(message)

                enemy.check_if_dead(self.name)

        self.board.backup_board[target[0]][target[1]] = self.weapon_sym

        return True

    def mid_p_f(self):

        for x in self.get_urdl_coords(self.y, self.x, 1):
            print(x)
        for x in self.get_around_coords(self.y, self.x, 1):
            print(x)
        input()

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

