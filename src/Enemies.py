from random import random, choice

from src.Living import Enemy


class Goblin(Enemy):

    def __init__(self):
        super().__init__()

        self.sym = 'g'
        self.name = "Goblin"

        self.moves = 3
        self.moves_per_turn = 3

        self.actions_per_turn = 2

        self.knife_sym = "k"
        self.knife_damage = 3

        self.twist_range = 1

        self.cards["Hit"] = {"func": self.hit,
                             "level": "weak"}

        self.cards["Quicker"] = {"func": self.quicker,
                                 "level": "medium"}

        self.cards["Twist"] = {"func": self.twist,
                               "level": "strong"}

        self.init_cards()

    def boss_maintance(self):

        self.is_boss()

        self.knife_damage *= 2
        self.twist_range *= 2

    def hit(self):

        if not self.can_attack:
            return

        coords = self.get_urdl_coords(self.y, self.x, 1)
        for coord in coords:

            ycor, xcor = coord[0][0], coord[0][1]

            target = self.check_coord(ycor, xcor)
            if target in self.board.allies:

                self.make_hit(target, ycor, xcor)

                return

    def make_hit(self, target, ycor, xcor):

        self.board.backup_board[ycor][xcor] = self.knife_sym

        if target.invulnerable or target.dead:
            return

        self.target.health -= self.knife_damage

        message = f"{self.name} dealt {self.knife_damage} damage to {target.name} with his knife."
        self.board.add_log(message)

        target.check_if_dead(self)

    def twist(self):

        if not self.can_attack:
            return

        coords = self.get_around_coords(self.y, self.x, self.twist_range)

        for coord in coords:

            target = self.check_coord(coord[0], coord[1])

            self.make_twist(coord[0], coord[1], target)

    def make_twist(self, ycor, xcor, target):

        if target == 'invalid':
            return

        self.board.backup_board[ycor][xcor] = self.knife_sym

        if target in self.board.allies:

            if target.invulnerable or target.dead:
                return

            target.health -= self.knife_damage

            message = f"{self.name} made a twist and dealt {self.knife_damage} to {target.name} with his knife."
            self.board.add_log(message)

            target.check_if_dead(self)

    def quicker(self):

        self.moves = max(self.moves+1, self.moves_per_turn+1)
        self.moves_changed_counter += 1


class Snake(Enemy):

    def __init__(self):
        super().__init__()

        self.name = 'Snake'
        self.sym = 'ç'
        self.poison_sym = 'p'

        self.health = 15

        self.poison_damage = 2
        self.poison_dot_damage = 1
        self.dot_turn_duration = 3
        self.spit_range = 5
        self.spray_range = 2

        self.bitten_allies = {}

        self.cards["Sting"] = {"func": self.sting,
                               "level": "weak"}

        self.cards["Spit"] = {"func": self.spit,
                              "level": "medium"}

        self.cards["Spray"] = {"func": self.spray,
                               "level": "strong"}

        self.init_cards()

    def boss_maintance(self):

        self.is_boss()

        self.poison_damage *= 2
        self.poison_dot_damage *= 2
        self.dot_turn_duration = 4
        self.spit_range = 8
        self.spray_range += 1

    def sting(self):

        if not self.can_attack:
            return

        coords = self.get_urdl_coords(self.y, self.x, 1)
        for coord in coords:

            ycor, xcor = coord[0][0], coord[0][1]
            target = self.check_coord(ycor, xcor)

            if target in self.board.allies:
                self.make_sting(target, ycor, xcor, True)
                return

    def make_sting(self, target, ycor=None, xcor=None, sym=False, message=None):

        if sym:
            self.board.backup_board[ycor][xcor] = self.poison_sym

        if target.invulnerable or target.dead:
            return

        message = message if message else f"{self.name} stung {target.name}. {target.name} is poisoned."
        self.board.add_log(message)

        self.bitten_allies[target] = self.dot_turn_duration

        if self.poison_dot not in self.board.living_turn_checker:
            self.board.living_turn_checker.append(self.poison_dot)

    def poison_dot(self, living):

        if living in self.board.enemies:
            return

        self.make_poison_dot(living)

        if len(self.bitten_allies) == 0:
            return True

    def make_poison_dot(self, target):

        if self.bitten_allies[target] == 0 or target.dead:
            del self.bitten_allies[target]
            return

        self.bitten_allies[target] -= 1

        if target.invulnerable:
            return

        target.health -= self.poison_dot_damage

        message = f"{self.name} dealt {self.poison_dot_damage} damage to {target.name} with its poison."
        self.board.add_log(message)

        target.check_if_dead(self)

    def spit(self):

        if not self.can_attack:
            return

        directions = self.get_urdl_coords(self.y, self.x, self.spit_range)
        for direction in directions:

            for index, coord in enumerate(direction):

                target = self.check_coord(coord[0], coord[1])

                if target == 'invalid':
                    break

                if target in self.board.allies:
                    self.make_spit(target, direction, index)
                    return

    def make_spit(self, target, direction, index):

        for coord in direction[:index+1]:
            self.board.backup_board[coord[0]][coord[1]] = self.poison_sym

        if target.invulnerable:
            return

        message = f"{self.name} spit on {target.name}. {target.name} is poisoned."
        self.make_sting(target, message=message)

        target.health -= self.poison_damage

        message = f"{self.name} dealt {self.poison_damage} damage to {target.name} with its venom spit."
        self.board.add_log(message)

        target.check_if_dead(self)

    def spray(self):

        if not self.can_attack:
            return

        coords = self.get_around_coords(self.y, self.x, self.spray_range)

        for coord in coords:

            target = self.check_coord(coord[0], coord[1])

            self.make_spray(coord[0], coord[1], target)

    def make_spray(self, ycor, xcor, target):

        if target == 'invalid':
            return

        self.board.backup_board[ycor][xcor] = self.poison_sym

        if target in self.board.allies:

            if target.invulnerable or target.dead:
                return

            message = f"{self.name} sprayed on {target.name}. {target.name} is poisoned."
            self.make_sting(target, message=message)

            target.health -= self.poison_damage

            message = f"{self.name} sprayed poison and dealt {self.poison_damage} to {target.name}."
            self.board.add_log(message)

            target.check_if_dead(self)


class Troll(Enemy):

    def __init__(self):
        super().__init__()

        self.name = 'Troll'
        self.sym = 'y'
        self.rock_sym = 'r'

        self.health = 30

        self.rock_damage = 4
        self.boulder_damage = 5
        self.splah_damage = 3

        self.throw_rock_range = 10
        self.throw_boulder_range = 6
        self.splash_range = 2

        self.cards["Throw Rock"] = {"func": self.throw_rock,
                                    "level": "weak"}

        self.cards["Rock Form"] = {"func": self.rock_form,
                                   "level": "medium"}

        self.cards["Throw Boulder"] = {"func": self.throw_boulder,
                                       "level": "strong"}

        self.init_cards()

    def boss_maintance(self):

        self.is_boss()

        self.rock_damage *= 2
        self.boulder_damage *= 2
        self.splah_damage *= 2

        self.throw_rock_range += 3
        self.throw_boulder_range += 2
        self.splash_range += 1

    def throw_rock(self, is_boulder=False):

        if not self.can_attack:
            return

        throw_range = self.throw_boulder_range if is_boulder else self.throw_rock_range
        directions = self.get_urdl_coords(self.y, self.x, throw_range)

        for direction in directions:

            for index, coord in enumerate(direction):

                target = self.check_coord(coord[0], coord[1])

                if target == 'invalid':
                    break

                if target in self.board.allies:
                    self.do_throw_rock(target, direction, index, is_boulder)
                    return coord[0], coord[1]

    def do_throw_rock(self, target, direction, index, is_boulder=False):

        for coord in direction[:index+1]:
            self.board.backup_board[coord[0]][coord[1]] = self.rock_sym

        if target.invulnerable:
            return

        damage = self.boulder_damage if is_boulder else self.rock_damage
        target.health -= damage

        message = f"{self.name} threw a {'boulder' if is_boulder else 'rock'} "\
                  f"on {target.name}, dealing {damage} damage."
        self.board.add_log(message)

        target.check_if_dead(self)

    def rock_form(self):

        self.health += 5

        message = f"{self.name} assumed his rock form, becoming more resilient."
        self.board.add_log(message)

    def throw_boulder(self):

        if not self.can_attack:
            return

        target_coords = self.throw_rock(is_boulder=True)

        if not target_coords:
            return

        ycoor, xcoor = target_coords
        around_coords = self.get_around_coords(ycoor, xcoor, self.splash_range)

        for coord in around_coords:

            target = self.check_coord(coord[0], coord[1])
            self.do_throw_boulder(coord[0], coord[1], target)

    def do_throw_boulder(self, ycor, xcor, target):

        if target == 'invalid':
            return

        self.board.backup_board[ycor][xcor] = self.rock_sym

        if target in self.board.allies:

            if target.invulnerable or target.dead:
                return

            target.health -= self.splah_damage

            message = f"{target.name} was hit by the splash of {self.name}'s"\
                      f"boulder throw, which dealt {self.splah_damage} damage."
            self.board.add_log(message)

            target.check_if_dead(self)


class Orc(Enemy):

    def __init__(self):
        super().__init__()

        self.sym = 'o'
        self.name = 'Orc'

        self.moves = 1
        self.moves_per_turn = 1

        self.actions = 2
        self.actions_per_turn = 2

        self.axe_default_damage = 3
        self.axe_damage = self.axe_default_damage

        self.axe_increased_damage = 5
        self.warcry_counter = 3
        self.axe_range = 1

        self.cards["Axe Swing"] = {"func": self.axe_swing,
                                   "level": "weak"}

        self.cards["Sprint"] = {"func": self.sprint,
                                "level": "medium"}

        self.cards["Warcry"] = {"func": self.warcry,
                                "level": "strong"}

        self.init_cards()

    def axe_swing(self):

        if not self.can_attack:
            return

        coords = self.get_around_coords(self.y, self.x, self.axe_range)

        for coord in coords:

            target = self.check_coord(coord[0], coord[1])

            self.do_axe_swing(coord[0], coord[1], target)

    def do_axe_swing(self, ycor, xcor, target):

        if target == 'invalid':
            return

        self.board.backup_board[ycor][xcor] = self.axe_sym

        if target in self.board.allies:

            if target.invulnerable or target.dead:
                return

            target.health -= self.axe_damage

            message = f"{self.name} swung his axe and dealt {self.axe_damage} damage to {target.name}."
            self.board.add_log(message)

            target.check_if_dead(self)

    def sprint(self):

        self.moves = max(self.moves+1, self.moves_per_turn+1)
        self.moves_changed_counter += 1

    def warcry(self):

        message = f"{self.name} unleashed his warcry, gaining temporary strengh."
        self.board.add_log(message)

        self.axe_damage = self.axe_increased_damage

        if self.warcry_checker not in self.board.living_turn_checker:
            self.board.living_turn_checker.append(self.warcry_checker)

    def warcry_checker(self, living):

        if self.warcry_counter == 0:
            self.warcry_counter = 3
            self.axe_damage = self.axe_default_damage
            return True

        if self == living:
            self.warcry_counter -= 1


class Necro(Enemy):

    def __init__(self):
        super().__init__()

        self.sym = 'n'
        self.name = 'Necromancer'

        self.health = 15

        self.moves = 0
        self.moves_per_turn = 0

        self.actions_per_turn = 1

        self.spell_sym = "d"
        self.drain_life_damage = 1

        self.cards["Drain Life"] = {"func": self.drain_life,
                                    "level": "weak"}

        self.cards["Reincarnate"] = {"func": self.reincarnate,
                                     "level": "medium"}

        self.cards["Summon Orc"] = {"func": self.summon_orc,
                                    "level": "strong"}

        self.init_cards()

    def boss_maintance(self):

        self.is_boss()

        self.drain_life_damage *= 1

    def drain_life(self):

        if not self.can_attack:
            return

        for ally in self.board.allies:

            if ally.invulnerable:
                continue

            chance = random()
            if chance < 0.5:
                continue

            self.do_drain_life(ally)

    def do_drain_life(self, ally):

        while True:

            enemy = choice(self.board.enemies)
            if enemy.dead:
                continue

            self.board.backup_board[ally.y][ally.x] = self.spell_sym
            self.board.backup_board[enemy.y][enemy.x] = self.heal_sym

            ally.health -= self.drain_life_damage
            enemy.health += self.drain_life_damage

            message = f"{self.name} drained {self.drain_life_damage} "\
                      f"life from {ally.name} and healed {enemy.name} "\
                      f"with the drained life."
            self.board.add_log(message)

            return

    def reincarnate(self):

        chance = random()
        if chance < 0.4:
            return

        for enemy in self.board.enemies:

            if not enemy.dead or enemy.revive_counter <= 0:
                continue

            self.revive_living(enemy)

            return

    def summon_orc(self):

        chance = random()
        if chance < 0.3:
            return

        self.summon_enemy_ally(Orc)

