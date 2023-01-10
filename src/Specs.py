from random import random

from Player import Player


class Warrior(Player):

    def __init__(self):
        super().__init__()

        self.sym = "W"
        self.name = "Warrior"
        self.weapon_sym = self.axe_sym
        self.ignore_sym = "i"
        self.short_taunt_duration = 3
        self.axe_damage = 5

        swing_axe = "Swings your axe hiting a single enemy."
        short_taunt = f"Taunts each enemy for {self.short_taunt_duration} "\
                      f"turn{'s' if self.short_taunt_duration > 1 else ''}."
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

            if (enemy.y, enemy.x) == (target[0], target[1]) and not enemy.dead:
                enemy.health -= self.axe_damage

                message = f"{self.name} dealt {self.axe_damage} damage to "\
                          f"{enemy.name} with his axe."
                self.board.add_log(message)

                enemy.check_if_dead(self)

        self.board.backup_board[target[0]][target[1]] = self.weapon_sym

        return True

    def taunt(self):

        message = "To taunt each oponent, enter '1'. To cancel, enter 'q': "
        go_on = self.yes_no_input(message)

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

        message = f"To taunt each oponent for {self.short_taunt_duration} "\
                  f"turns, enter '1'. To cancel, enter 'q': "
        go_on = self.yes_no_input(message)

        if not go_on:
            return

        self.do_short_taunt()

        return True

    def inner_ignore_pain(self, living):

        if not living == self:
            return

        self.invulnerable = False

        message = f"{self.name} is no longe invulnerable."
        self.board.add_log(message)

        return True

    def ignore_pain(self):

        message = "To ignore pain until your next turn, enter '1'. "\
                  "To cancel, enter 'q': "
        go_on = self.yes_no_input(message)

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

            self.invulnerable = False

            message = f"{self.name}'s Avoid Pain period ended."
            self.board.add_log(message)

            return True

        if random() > 0.5:
            self.invulnerable = True
        else:
            self.invulnerable = False

    def avoid_pain(self):

        input_message = "To avoid damage until your next turn, enter '1'. "\
                        "To cancel, enter 'q': "
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

        self.silence_duration = 2
        self.silence_turns = self.silence_duration

        blessing = f'Heals an ally for {self.blessing_heal} '\
                   f'for {self.blessing_turns}.'
        silence = f"Silence enemies, impairing their attacks."
        light_heal = f'Heals an ally for {self.light_heal_heal}.'
        all_healed = f'Heals each ally for {self.all_healed_heal}.'
        revive = f"Revive a dead player if not alive "\
                 f"for {self.revive_turns} turns."

        self.cards["Blessing"] = {"func": self.blessing,
                                  "descr": blessing,
                                  "level": "weak"}

        self.cards["Silence"] = {"func": self.silence,
                                 "descr": silence,
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

        message = f'{self.name} healed {living.name} for '\
                  f'{self.blessing_heal} with blessing.'
        self.board.add_log(message)

    def silence(self):

        question = f"Do you wish to silence enemies, impairing their attacks "\
                   f"for {self.silence_duration} turns?"\
                   f"Enter '1' for yes or 'q' for no."

        go_on = self.yes_no_input(question)

        if not go_on:
            return

        for enemy in self.board.enemies:
            enemy.can_attack = False

        message = f"{self.name} silenced enemies, impairing their attacks."
        self.board.add_log(message)

        self.append_to_turn_checker(self.cancel_silence)

        return True

    def cancel_silence(self, living):

        if self != living:
            return

        self.silence_turns -= 1

        if self.silence_turns == 0:
            self.silence_turns = self.silence_duration
            return True

    def light_heal(self):

        question = "Which ally would you like to light heal?"
        ally = self.prompt_for_ally(question)

        if not ally:
            return

        ally.health += self.light_heal_heal
        self.board.backup_board[ally.y][ally.x] = self.heal_sym

        message = f"{self.name} healed {ally.name} for "\
                  f"{self.light_heal_heal} health."
        self.board.add_log(message)

        return True

    def all_healed(self):

        message = "Do you want to heal all allies?\n"\
                  "Enter '1' for yes and 'q' for no:"
        answer = self.yes_no_input(message)

        if not answer:
            return

        message = f"{self.name} healed "

        for ind, ally in enumerate(self.board.allies):
            ally.health += self.all_healed_heal
            self.board.backup_board[ally.y][ally.x] = self.heal_sym
            message += f"{ally.name}"\
                       f"{'.' if ind == len(self.board.allies)-1 else ', '}"

        self.board.add_log(message)

        return True

    def revive(self):

        dead_players = [player for player in self.board.players
                        if player.dead and player.revive_counter > 0]

        if len(dead_players) == 0:
            self.clear_screen()
            input("Not enough dead players.\n\nPress 'Enter' to continue.")
            return

        question = "Which ally do you want to revive?"
        ally = self.prompt_for_ally(question, dead_players)

        if not ally:
            return

        if ally.revive_counter <= 0:
            input("Enemy can't be revived\n\nPress 'Enter' to continue.")
            return

        if self.revive_living(ally):
            return True


class Rogue(Player):

    def __init__(self):
        super().__init__()

        self.sym = "R"
        self.name = "Rogue"

        self.health = 15

        self.throw_range = 4
        self.knife_damage = 3
        self.arrow_damage = 4

        self.fade_out_turns = 4

        self.enemies_hit = []

        multi_target = "If it's the first time this turn you've hit "\
                       "this enemy, gain this ability again."

        knife_throw = f"Jumps and throws a knife at an enemy. {multi_target}"
        arrow_shot = f"Jumps and shots an arrow at an enemy. {multi_target}"
        knives_out = f"Jumps and slashes all enemies. {multi_target}"
        blades_dance = f"Jumps and throws four knives. {multi_target}"
        fade_out = "Becomes invisible for your enemies."

        self.cards["Knife Throw"] = {"func": self.knife_throw,
                                     "descr": knife_throw,
                                     "level": "weak"}

        self.cards["Arrow Shot"] = {"func": self.arrow_shot,
                                    "descr": arrow_shot,
                                    "level": "medium"}

        self.cards["Knives Out"] = {"func": self.knives_out,
                                    "descr": knives_out,
                                    "level": "medium"}

        self.cards["Fade out"] = {"func": self.fade_out,
                                  "descr": fade_out,
                                  "level": "strong"}

        self.cards["Blades Dance"] = {"func": self.blades_dance,
                                      "descr": blades_dance,
                                      "level": "strong"}

        self.init_cards()

    def fade_out(self):

        question = "Do you wish to fade out, becoming invisible? "\
                   "Enter '1' for yes or 'q' for no."
        go_on = self.yes_no_input(question)

        if not go_on:
            return

        self.can_be_target = False

        self.append_to_turn_checker(self.fade_out_check)

        message = f"{self.name} faded out and became invisible."
        self.board.add_log(message)

        return True

    def fade_out_check(self, living):

        if self != living:
            return

        self.fade_out_turns -= 1

        if self.fade_out_turns == 0:
            return True

    def empty_targets(self, living):

        if living != self:
            return

        self.enemies_hit = []

        return True

    def check_multi_target(self, target, card):

        if target in self.enemies_hit:
            return

        self.enemies_hit.append(target)
        self.append_to_turn_checker(self.empty_targets)
        self.my_cards.append(card)
        self.actions += 1

    def knife_throw(self):

        card = "Knife Throw"
        message = f"{self.name} dealt {self.knife_damage} damage "\
                  "to # with knife throw."

        side = self.prompt_direction()

        if not side:
            return

        direction = self.get_urdl_coords(self.y, self.x,
                                         self.throw_range)[side-1]
        target = self.fill_line_until_hit(direction, self.knife_sym,
                                          self.knife_damage, message)
        if target:
            self.check_multi_target(target, card)

        self.jump_func()

        return True

    def arrow_shot(self):

        card = "Arrow Shot"
        message = f"{self.name} dealt {self.knife_damage} damage "\
                  "to # with arrow shot."

        side = self.prompt_direction()

        if not side:
            return

        direction = self.get_urdl_coords_all(self.y, self.x)[side-1]
        target = self.fill_line_until_hit(direction, self.arrow_sym,
                                          self.arrow_damage, message)
        if target:
            self.check_multi_target(target, card)

        self.jump_func()

        return True

    def knives_out(self):

        card = "Knives Out"
        message = f"{self.name} dealt {self.knife_damage} damage "\
                  "to # with knives out."
        question = "Do you wish to hit all enemies around you with knives " \
                   "out?\nEnter '1' for yes or 'q' for no."

        self.player_around_damage(1, self.knife_sym, self.knife_damage, message,
                                  question, self.check_multi_target, card)

        self.jump_func()

        return True

    def blades_dance(self):

        card = "Blades Dance"
        message = f"{self.name} dealt {self.knife_damage} damage "\
                  "to # with blades dance."
        question = "Do you wish to throw 4 knives at the enemies around you?" \
                   "out?\nEnter '1' for yes or 'q' for no."

        go_on = self.yes_no_input(question)

        if not go_on:
            return

        directions = self.get_urdl_coords(self.y, self.x, self.throw_range)

        for direction in directions:
            for coord in direction:

                target = self.do_player_damage(coord, self.knife_sym,
                                               self.knife_damage, message)

                if target:
                    check_multi_target(target, card)

        self.jump_func()

        return True

