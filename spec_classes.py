from random import random

from player_class import Player

# self.cards = {"card_name": {"func": self.func, "descr": self.var, "level": "weak"},


class Warrior(Player):

    def __init__(self):
        super().__init__()

        self.sym = "W"
        self.name = "Warrior"
        self.weapon_sym = "x"
        self.taunt_sym = "t"
        self.ignore_sym = "i"
        self.short_taunt_duration = 3

        swing_axe = "Swings your axe hiting a single enemy."
        short_taunt = f"Taunts each enemy for {self.short_taunt_duration} turns."
        avoid_pain = "Tries to ignore all damage until your next turn"
        taunt = "Taunts each enemy."
        ignore_pain = "Ignores all damage until your next turn."

        self.cards["Axe Swing"] = {"func": self.swing_axe,
                                   "descr": swing_axe,
                                   "level": "weak"}

        self.cards["Avoid Pain"] = {"func": self.avoid_pain,
                                    "descr": avoid_pain,
                                    "level": "medium"}

        self.cards["Short Taunt"] = {"func": self.short_taunt,
                                     "descr": short_taunt,
                                     "level": "medium"}

        self.cards["Taunt"] = {"func": self.taunt,
                               "descr": taunt,
                               "level": "strong"}

        self.cards["Ignore Pain"] = {"func": self.ignore_pain,
                                     "descr": ignore_pain,
                                     "level": "strong"}

        self.init_cards()

    def swing_axe(self):

        damage = 5

        valid_input = self.prompt_direction()

        if not valid_input:
            return

        target = self.get_urdl_coords(self.y, self.x, 1)[valid_input-1][0]

        for enemy in self.board.enemies:

            if ((enemy.y, enemy.x) == (target[0], target[1])) and not enemy.dead:
                enemy.health -= damage

                message = f"{self.name} dealt {damage} damage to {enemy.name} with his axe."
                self.board.add_log(message)

                enemy.check_if_dead(self.name)

        self.board.backup_board[target[0]][target[1]] = self.weapon_sym

        return True

    def taunt(self):

        input_message = "To taunt each oponent, enter '1'. To cancel, enter 'q': "
        go_on = self.yes_no_input(input_message)

        if not go_on:
            return

        for enemy in self.board.enemies:

            enemy.target = self
            enemy.target_counter = 0
            self.board.backup_board[enemy.y][enemy.x] = self.taunt_sym

        message = f"{self.name} taunted each enemy."
        self.board.add_log(message)

        return True

    def short_taunt(self):

        input_message = f"To taunt each oponent for {self.short_taunt_duration} turns, enter '1'. To cancel, enter 'q': "
        go_on = self.yes_no_input(input_message)

        if not go_on:
            return

        for enemy in self.board.enemies:

            enemy.target = self
            enemy.target_counter = enemy.max_target_counter-self.short_taunt_duration-1
            self.board.backup_board[enemy.y][enemy.x] = self.taunt_sym

        message = f"{self.name} taunted each enemy for {self.short_taunt_duration} turns."
        self.board.add_log(message)

        return True

    def inner_ignore_pain(self, living):

        if not living == self:
            return

        self.invulnerable = False

        message = f"{self.name} is no longe invulnerable."
        self.board.add_log(message)

        return True

    def ignore_pain(self):

        input_message = "To ignore pain until next turn, enter '1'. To cancel, enter 'q': "
        go_on = self.yes_no_input(input_message)

        if not go_on:
            return

        self.invulnerable = True

        self.board.living_turn_checker.append(self.inner_ignore_pain)

        self.board.backup_board[self.y][self.x] = self.ignore_sym

        message = f"{self.name} is invulnerable until his next turn."
        self.board.add_log(message)

        return True

    def inner_avoid_pain(self, living):

        if living == self:
            self.invulnerable == False

            message = f"{self.name}'s Avoid Pain period ended."
            self.board.add_log(message)

            return True

        if random() > 0.5:
            self.invulnerable = True
        else:
            self.invulnerable = False

    def avoid_pain(self):

        input_message = "To avoid damage until your next turn, enter '1'. To cancel, enter 'q': "
        go_on = self.yes_no_input(input_message)

        if not go_on:
            return

        self.board.living_turn_checker.append(self.inner_avoid_pain)

        self.board.backup_board[self.y][self.x] = self.ignore_sym

        message = f"{self.name}'s Avoid Pain period started."
        self.board.add_log(message)

        return True


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

