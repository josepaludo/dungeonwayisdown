from random import choice

from src.Player import Player, Ally


class Demon(Ally):

    def __init__(self):
        super().__init__()

    def search_urdl_for_valid_enemy(self):

        directions = self.get_urdl_coords_all(self.y, self.x)

        for direction in directions:

            for coord in direction:

                target = self.check_coord(coord[0], coord[1])

                if target == 'invalid':
                    break

                if target in self.board.enemies:
                    return direction

    def burn_square(self, coord, message):

        ycor, xcor = coord[0], coord[1]
        target = self.check_coord(ycor, xcor)

        if target == 'invalid':
            return

        self.board.backup_board[ycor][xcor] = self.fire_sym

        if target in self.board.enemies:
            self.apply_fire_damage(target, message)
            return target

    def apply_fire_damage(self, target, message):

        target.health -= self.fire_damage

        message = message.split("#")
        message = message[0] + target.name + message[1]
        self.board.add_log(message)

        target.check_if_dead(self)

    def damage_around_enemy(self, enemy, reach, message, self_exc=True):

        coords = self.get_around_coords(enemy.y, enemy.x, reach, self_exc)

        for coord in coords:

            self.burn_square(coord, message)

    def damage_around_all_enemies(self, message, reach=1):

        for enemy in self.board.enemies:

            coords = self.get_around_coords(enemy.y, enemy.x, reach, False)

            for coord in coords:

                self.burn_square(coord, message)

    def meteor(self, reach=1):

        target = choice(self.board.enemies)

        message = f"{self.name} dealt {self.fire_damage} damage "\
                  f"to # with meteor fall."
        self.damage_around_enemy(target, reach, message, False)

    def fire_ball(self):

        direction = self.search_urdl_for_valid_enemy()
        message = f"{self.name} dealt {self.fire_damage} "\
                  f"damage to # with fire ball."

        if not direction:
            return

        for coord in direction:

            target = self.burn_square(coord, message)

            if target:
                self.damage_around_enemy(target, 1, message)
                return

    def meteor_fall(self):

        self.meteor()


class Imp(Demon):

    def __init__(self):
        super().__init__()

        self.sym = 'v'
        self.name = "Imp"

        self.health = 5
        self.fire_damage = 1

        self.cards["Fire Blast"] = {"func": self.fire_blast,
                                    "level": "weak"}

        self.cards["Fire Ball"] = {"func": self.fire_ball,
                                   "level": "medium"}

        self.cards["Meteor Fall"] = {"func": self.meteor_fall,
                                     "level": "strong"}

        self.init_cards()

    def fire_blast(self):

        direction = self.search_urdl_for_valid_enemy()
        message = f"{self.name} dealt {self.fire_damage} "\
                  f"damage to # with fire blast."

        if not direction:
            return

        for coord in direction:

            if self.burn_square(coord, message):
                return


class Infernal(Demon):

    def __init__(self):
        super().__init__()

        self.sym = 'j'
        self.name = "Infernal"

        self.health = 15
        self.fire_damage = 1

        self.cards["Meteor Fall"] = {"func": self.meteor_fall,
                                     "level": "weak"}

        self.cards["Double Meteor"] = {"func": self.double_meteor,
                                       "level": "medium"}

        self.cards["Meteor Rain"] = {"func": self.meteor_rain,
                                     "level": "strong"}

        self.init_cards()

    def double_meteor(self):

        for i in range(2):
            self.meteor_fall()

    def meteor_rain(self):

        message = f"{self.name} dealt {self.fire_damage} damage "\
                  f"to # with meteor rain."

        self.damage_around_all_enemies(message)


class Wizard(Player):

    def __init__(self):
        super().__init__()

        self.sym = "Z"
        self.name = "Wizard"

        self.fire_damage = 4
        self.lightning_damage = 5

        self.fire_ball_reach = 2
        self.meteor_rain_reach = 1

        summon_imp = "Summons an imp that has low life and deals low damage."
        fire_ball = "Throws a fireball that explodes on hit."
        lightning_bolt = "Casts a lightning bolt in all directions."
        meteor_rain = "Casts meteors from above."
        summon_infernal = "Summon an infernal demon."

        self.cards["Summon Imp"] = {"func": self.summon_imp,
                                    "descr": summon_imp,
                                    "level": "weak"}

        self.cards["Fire Ball"] = {"func": self.fire_ball,
                                   "descr": fire_ball,
                                   "level": "medium"}

        self.cards["Lightning Bolt"] = {"func": self.lightning_bolt,
                                        "descr": lightning_bolt,
                                        "level": "medium"}

        self.cards["Meteor Rain"] = {"func": self.meteor_rain,
                                     "descr": meteor_rain,
                                     "level": "strong"}

        self.cards["Summon Infernal"] = {"func": self.summon_infernal,
                                         "descr": summon_infernal,
                                         "level": "strong"}

        self.init_cards()

    def fire_ball(self):

        question = "Do you wish to cast a fire ball? "\
                   "Enter '1' for yes or 'q' for no."
        go_on = self.yes_no_input(question)

        if not go_on:
            return

        mess = f"{self.name} dealt {self.fire_damage} to # with fireball."
        target = self.find_enemy_in_line(self.fire_sym, self.fire_damage, mess)

        if not target:
            return

        coords = self.get_around_coords(target.y, target.x,
                                        self.fire_ball_reach)

        for coord in coords:

            self.do_player_damage(coord, self.fire_sym,
                                  self.fire_damage, mess)

        return True

    def lightning_bolt(self):

        question = "Do you wish to cast a lightning bolt?"\
                   " Enter '1' for yes or 'q' for no."
        go_on = self.yes_no_input(question)

        if not go_on:
            return

        message = f"{self.name} dealt {self.lightning_damage} damage to # "\
                  f"with lightning bolt."

        directions = self.get_urdl_coords_all(self.y, self.x)
        for direction in directions:
            for coord in direction:

                self.do_player_damage(coord, self.lightning_sym,
                                      self.lightning_damage, message)

        return True

    def meteor_rain(self):

        question = "Do you wish to cast meteor rain?"\
                   " Enter '1' for yes or 'q' for no."
        go_on = self.yes_no_input(question)

        if not go_on:
            return

        message = f"{self.name} dealt {self.fire_damage} damage to # "\
                  f"with meteor rain."

        self.damage_around_enemies(self.meteor_rain_reach, self.fire_sym,
                                   self.fire_damage, message)

        return True

    def summon_demon(self, is_imp):

        demon = Imp if is_imp else Infernal
        demon_name = "Imp" if is_imp else "Infernal"

        question = f"Do you want to summon a {demon_name} demon? "\
                   "Enter '1' for yes or 'q' for no."
        go_on = self.yes_no_input(question)

        if not go_on:
            return

        self.summon_enemy_ally(demon, is_enemy=False)

        return True

    def summon_imp(self):

        if self.summon_demon(is_imp=True):
            return True

    def summon_infernal(self):

        if self.summon_demon(is_imp=False):
            return True

