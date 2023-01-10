from random import choice, random


class Living:

    def __init__(self):

        self.x = None
        self.y = None
        self.sym = ""
        self.name = None

        self.heal_sym = 'h'
        self.invulnerable_sym = 'i'
        self.axe_sym = 'x'
        self.claw_sym = 'c'
        self.taunt_sym = 't'
        self.fire_sym = 'f'
        self.lightning_sym = 'l'
        self.knife_sym = 'k'
        self.arrow_sym = 'q'

        self.health = 20
        self.dead = False
        self.invulnerable = False
        self.can_attack = True
        self.can_move = True

        self.revive_counter_start = 4
        self.revive_counter = self.revive_counter_start
        self.summon_counter = 8
        self.can_be_target = True

        self.min_distance = 1
        self.current_distance = None
        self.current_directions = None
        self.valid_move_options = []
        self.closer_move_options = []

        self.moves = 1
        self.moves_per_turn = 1
        self.moves_changed_counter = 0

        self.actions = 1
        self.actions_per_turn = 1
        self.actions_changed_counter = 0

        self.max_target_counter = 5
        self.target_counter = self.max_target_counter

        self.board = None

        self.cards = {}
        self.card_list = []
        self.my_cards = []
        self.weak_cards, self.medium_cards, self.strong_cards = [], [], []

    def set_boss_name(self):

        self.name = f"{self.board.pick_name()}, the "\
                    f"{self.board.pick_boss_epithet()} {self.name}"

    def set_name(self):

        self.name = f"{self.board.pick_name()}, the {self.name}"

    def clear_screen(self):

        self.board.print_board()
        print(f"{self.sym}'s turn.\n")

    def check_coord(self, ycor, xcor):

        if self.board.board[ycor][xcor] == self.board.wall_square:
            return 'invalid'

        for living in self.board.livings:
            if (living.y, living.x) == (ycor, xcor):
                return living

    def get_urdl_coords_all(self, ycor, xcor):

        up = [(ycor-i-1, xcor) for i in range(ycor)]
        down = [(ycor+i+1, xcor) for i in range(len(self.board.board)-1-ycor)]
        left = [(ycor, xcor-i-1) for i in range(xcor)]
        right = [(ycor, xcor+i+1) for i in range(len(self.board.board[0])-1-xcor)]

        return up, right, down, left

    def get_urdl_coords(self, ycor, xcor, rangei):

        up, right, down, left = self.get_urdl_coords_all(ycor, xcor)

        return up[:rangei], right[:rangei], down[:rangei], left[:rangei]

    def get_around_coords(self, ycor, xcor, rangei, self_exc=True):

        yrange = range(ycor-rangei, ycor+rangei+1)
        xrange = range(xcor-rangei, xcor+rangei+1)

        coords = [(y, x) for y in yrange for x in xrange]
        valids = [yx for yx in coords if 0 < yx[0] < 19 and 0 < yx[1] < 19]

        if self_exc and (ycor, xcor) in valids:
            valids.remove((ycor, xcor))

        return valids

    def prompt_direction(self):

        while True:

            self.clear_screen()
            print("Directions:\n\n'1' for up.\n'2' for right.\n"
                  "'3' for down.\n'4' for left.\n\n'q' to quit.")

            direction = input("\nEnter chosen direction: ")

            if direction == 'q':
                return

            if self.check_int_range(direction, 1, 4):
                return int(direction)

            self.wrong_input_warning()

    def check_int_range(self, inp, start=None, end=None):

        try:
            inp = int(inp)
        except ValueError:
            self.wrong_input_warning()
            return

        if not start:
            return True

        if start <= inp <= end:
            return True

    def wrong_input_warning(self):

        self.clear_screen()
        print("Invalid input. Try again.")
        input("\nPress 'Enter' to continue.")

    def yes_no_input(self, input_message, yes_par='1', no_par='q'):

        while True:

            self.clear_screen()
            print(input_message)
            input_ = input()

            if input_ == yes_par:
                return True

            if input_ == no_par:
                return False

            self.wrong_input_warning()

    def check_if_dead(self, killer=None):

        if self.health > 0:
            return

        self.dead = True
        self.board.board[self.y][self.x] = self.board.empty_square

        message = f"{self.name} died.{f' {killer.name} slayed it.' if killer else ''}"
        self.board.add_log(message)

        return True

    def init_cards(self):

        self.strong_cards = [card for card, info in self.cards.items() if info['level'] == 'strong']
        self.medium_cards = [card for card, info in self.cards.items() if info['level'] == 'medium']
        self.weak_cards = [card for card, info in self.cards.items() if info['level'] == 'weak']

    def get_turn_cards(self):

        chance = random()

        no_cards, weak, medium = 0, 0.5, 0.85

        if chance == no_cards:
            message = f"{self.name} couldn't draw a card."
            self.board.add_log(message)
        elif chance < weak:
            self.my_cards.append(choice(self.weak_cards))
        elif chance < medium:
            self.my_cards.append(choice(self.medium_cards))
        else:
            self.my_cards.append(choice(self.strong_cards))

    def revive_living(self, living):

        coords = self.get_urdl_coords(self.y, self.x, 1)

        for coord in coords:

            ycor, xcor = coord[0][0], coord[0][1]

            if not self.board.board[ycor][xcor] == self.board.empty_square:
                continue

            living.reset_self_values(ycor, xcor)

            message = f"{self.name} revived {living.name}."
            self.board.add_log(message)

            return True

    def reset_self_values(self, ycor, xcor):

        self.revive_counter = self.revive_counter_start
        self.board.board[ycor][xcor] = self.sym
        self.dead = False
        self.invulnerable = False
        self.can_attack = True
        self.can_move = True
        self.y, self.x = ycor, xcor
        self.health = 15

    def set_target(self, is_enemy=True):

        if self.target_counter < self.max_target_counter:

            self.target_counter += 1
            return True

        livings = self.board.allies if is_enemy else self.board.enemies
        targets = [living for living in livings
                   if not living.dead and living.can_be_target]

        if len(targets) == 0:
            return

        self.target = choice(targets)
        self.target_counter = 0

        return True

    def distance(self, coor):

        xdiff = abs(coor[1]-self.target.x)
        ydiff = abs(coor[0]-self.target.y)

        return xdiff+ydiff

    def measure_distance(self):

        self.current_distance = self.distance((self.y, self.x))

        up, down = (self.y-1, self.x), (self.y+1, self.x)
        left, right = (self.y, self.x-1), (self.y, self.x+1)

        self.current_directions = up, right, down, left

    def try_to_approach(self):

        if self.current_distance == self.min_distance:
            return

        self.valid_move_options = []
        self.closer_move_options = []

        for direction in self.current_directions:

            self.check_if_valid_or_closer(direction)

        return True

    def check_if_valid_or_closer(self, direc):

        location = self.board.board[direc[0]][direc[1]]
        if location not in [self.board.empty_square, self.board.hole_square]:
            return

        self.valid_move_options.append(direc)

        if self.distance(direc) >= self.current_distance:
            return

        if location == self.board.empty_square:
            self.closer_move_options.append(direc)

    def choose_direction(self):

        if len(self.valid_move_options + self.closer_move_options) == 0:
            return

        if len(self.closer_move_options) == 0:
            return choice(self.valid_move_options)

        return choice(self.closer_move_options)

    def make_the_move(self, direc):

        self.board.board[self.y][self.x] = self.board.empty_square

        if self.board.board[direc[0]][direc[1]] == self.board.hole_square:
            self.hole_fall()
            return

        self.y, self.x = direc[0], direc[1]
        self.board.board[self.y][self.x] = self.sym

    def turn_move(self, is_enemy):

        if not self.set_target(is_enemy):
            return

        self.measure_distance()

        if not self.try_to_approach():
            return

        direction = self.choose_direction()

        if not direction:
            return

        self.make_the_move(direction)

    def empty_hand(self):

        self.my_cards = []

    def hole_fall(self):

        self.health = 0
        report = f"{self.name} fell in a hole."
        self.board.add_log(report)

    def living_maintance(self, is_enemy):

        for i in range(self.actions_per_turn):
            self.get_turn_cards()

        self.actions = max(self.actions, self.actions_per_turn)
        self.moves = max(self.moves, self.moves_per_turn)

        if is_enemy:
            return True

        self.summon_counter -= 1

        if self.summon_counter > 0:
            return True

        self.health = 0
        self.check_if_dead()

    def summon_enemy_ally(self, summon_class, is_enemy=True):

        coords = self.get_urdl_coords(self.y, self.x, 1)

        for coord in coords:

            ycor, xcor = coord[0][0], coord[0][1]

            if not self.board.board[ycor][xcor] == self.board.empty_square:
                continue

            self.do_summon_enemy_ally(summon_class, ycor, xcor, is_enemy)

            return

    def do_summon_enemy_ally(self, summon_class, ycor, xcor, is_enemy):

        summon = summon_class()
        summon.y, summon.x = ycor, xcor
        summon.board = self.board
        summon.name = self.board.pick_name()

        self.board.board[ycor][xcor] = summon.sym
        self.board.livings.append(summon)

        group = self.board.enemies if is_enemy else self.board.allies
        group.append(summon)

        message = f"{self.name} summoned {summon.name}."
        self.board.add_log(message)

    def urdl_damage(self, sym, damage, weapon, is_enemy=True, only_one=True):

        if not self.can_attack:
            return

        coords = self.get_urdl_coords(self.y, self.x, 1)

        for coord in coords:

            ycor, xcor = coord[0][0], coord[0][1]
            target = self.check_coord(ycor, xcor)
            target_group = self.board.allies if is_enemy else self.board.enemies

            if target not in target_group:
                continue

            self.do_urdl_damage(sym, damage, weapon, target, ycor, xcor)

            if only_one:
                return

    def do_urdl_damage(self, sym, damage, weapon, target, ycor, xcor):

        if target.dead:
            return

        self.board.backup_board[ycor][xcor] = sym

        if target.invulnerable:
            return

        self.target.health -= damage

        message = f"{self.name} dealt {damage} damage to {target.name} with its {weapon}."
        self.board.add_log(message)

        target.check_if_dead(self)

    def around_damage(self, sym, damage, weapon, is_enemy=True, range_=1):

        if not self.can_attack:
            return

        coords = self.get_around_coords(self.y, self.x, range_)

        for coord in coords:

            ycor, xcor = coord[0], coord[1]
            target = self.check_coord(ycor, xcor)
            target_group = self.board.allies if is_enemy else self.board.enemies

            self.do_around_damage(sym, damage, weapon, ycor, xcor, target, target_group)

    def do_around_damage(self, sym, damage, weapon, ycor, xcor, target, target_group):

        if target == 'invalid':
            return

        self.board.backup_board[ycor][xcor] = sym

        if target not in target_group:
            return

        if target.invulnerable or target.dead:
            return

        target.health -= damage

        message = f"{self.name} dealt {damage} damage to {target.name} with its {weapon}."
        self.board.add_log(message)

        target.check_if_dead(self)

    def do_short_taunt(self):

        for enemy in self.board.enemies:

            enemy.target = self
            enemy.target_counter = enemy.max_target_counter-self.short_taunt_duration-1
            self.board.backup_board[enemy.y][enemy.x] = self.taunt_sym

        message = f"{self.name} taunted each enemy for {self.short_taunt_duration} turns."
        self.board.add_log(message)

    def barkskin(self):

        self.health += self.barkskin_health

        message = f"{self.name} toughens its skin, becoming more resilient."
        self.board.add_log(message)


class Enemy(Living):

    def __init__(self):
        super().__init__()

        self.player_or_enemy = 'Enemy'

        self.sym = "e"
        self.name = "Generic small enemy"

    def is_boss(self):

        self.player_or_enemy = 'Boss'
        self.sym = self.sym.title()
        self.name += " Boss"
        self.health *= 2
        self.moves_per_turn *= 2
        self.actions_per_turn *= 2

