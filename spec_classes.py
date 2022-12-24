from random import random

from player_class import Player

# self.cards = {"card_name": {"func": self.func, "descr": self.var, "level": "weak"},


class Warrior(Player):

    def __init__(self):
        super().__init__()

        self.sym = "W"
        self.name = "Warrior"
        self.weapon_sym = self.axe_sym
        self.taunt_sym = "t"
        self.ignore_sym = "i"
        self.short_taunt_duration = 3
        self.axe_damage = 5

        swing_axe = "Swings your axe hiting a single enemy."
        short_taunt = f"Taunts each enemy for {self.short_taunt_duration} turn{'s' if self.short_taunt_duration > 1 else ''}."
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

        valid_input = self.prompt_direction()

        if not valid_input:
            return

        target = self.get_urdl_coords(self.y, self.x, 1)[valid_input-1][0]

        for enemy in self.board.enemies:

            if ((enemy.y, enemy.x) == (target[0], target[1])) and not enemy.dead:
                enemy.health -= self.axe_damage

                message = f"{self.name} dealt {self.axe_damage} damage to {enemy.name} with his axe."
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

        if self.invulnerable:
            self.clear_screen()
            input("You are already invulnerable.\nPress 'Enter' to continue.")
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
        self.name = 'Priest'

        self.blessing_allies = {}
        self.protect_allies = []

        self.blessing_turns = 4
        self.blessing_heal = 1
        self.protect_turns = 1
        self.light_heal_heal = 5
        self.all_healed_heal = 3
        self.revive_turns = 3

        blessing = f'Heals an ally for {self.blessing_heal} for {self.blessing_turns}.'
        protect = 'Make an ally invulnerable for 1 turn.'
        light_heal = f'Heals an ally for {self.light_heal_heal}.'
        all_healed = f'Heals each ally for {self.all_healed_heal}.'
        revive = f"Revive a dead player if not alive for {self.revive_turns} turns."

        self.cards["Blessing"] = {"func": self.blessing,
                                  "descr": blessing,
                                  "level": "weak"}

        self.cards["Protect"] = {"func": self.protect,
                                 "descr": protect,
                                 "level": "medium"}

        self.cards["Light Heal"] = {"func": self.light_heal,
                                    "descr": light_heal,
                                    "level": "medium"}

        self.cards["All Healed"] = {"func": self.all_healed,
                                    "descr": all_healed,
                                    "level": "strong"}

        self.cards["Revive"] = {"func": self.revive,
                                  "descr": revive,
                                  "level": "strong"}

        self.init_cards()

    def blessing(self):

        question = "Which ally would you like to bless?"

        ally = self.prompt_for_ally(question)

        if not ally:
            return

        self.apply_blessing(ally)

        return True

    def apply_blessing(self, ally):

        self.blessing_allies[ally] = self.blessing_turns

        if self.do_blessing not in self.board.living_turn_checker:
            self.board.living_turn_checker.append(self.do_blessing)

        message = f"{self.name} blessed {ally.name}."
        self.board.add_log(message)

        self.board.backup_board[ally.y][ally.x] = self.heal_sym

    def do_blessing(self, living):

        if living not in self.blessing_allies:
            return

        if self.blessing_allies[living] == 0:
            del self.blessing_allies[living]

        if len(self.blessing_allies) == 0:
            return True

        self.blessing_allies[living] -= 1
        living.health += self.blessing_heal

        message = f'{self.name} healed {living.name} for {self.blessing_heal} with blessing.'
        self.board.add_log(message)

    def protect(self):

        question = "Which ally would you like to protect?"

        ally = self.prompt_for_ally(question)

        if not ally:
            return

        self.apply_protect(ally)

        return True

    def apply_protect(self, ally):

        if self.do_protect not in self.board.living_turn_checker:
            self.board.living_turn_checker.append(self.do_protect)

        message = f"{self.name} protected {ally.name}."
        self.board.add_log(message)

        self.board.backup_board[ally.y][ally.x] = self.invulnerable_sym
        self.protect_allies.append(ally)
        ally.invulnerable = True

    def do_protect(self, living):

        if not living == self:
            return

        for ally in self.protect_allies:
            ally.invulnerable = False

            message = f'{ally.name} is no longer protected by {self.name}.'
            self.board.add_log(message)

        return True

    def light_heal(self):

        question = "Which ally would you like to light heal?"
        ally = self.prompt_for_ally(question)

        if not ally:
            return

        ally.health += self.light_heal_heal
        self.board.backup_board[ally.y][ally.x] = self.heal_sym

        message = f"{self.name} healed {ally.name} for {self.light_heal_heal} health."
        self.board.add_log(message)

        return True

    def all_healed(self):

        message = "Do you want to heal all allies?\nEnter '1' for yes and 'q' for no:"
        answer = self.yes_no_input(message)

        if not answer:
            return

        message = f"{self.name} healed "

        for ind, ally in enumerate(self.board.allies):
            ally.health += self.all_healed_heal
            message += f"{ally.name}{'.' if ind == len(self.board.allies)-1 else ', '}"

        self.board.add_log(message)

        return True

    def revive(self):

        dead_players = [player for player in self.board.players if players.dead and player.revive_counter > 0]

        if len(dead_players) == 0:
            self.clear_screen()
            input("Not enough dead players.\n\nPress 'Enter' to continue.")
            return

        question = "Which ally do you want to revive?"
        ally = self.prompt_for_ally(question, dead_players)

        if not ally:
            return

        if self.revive_living(ally):
            return True

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

