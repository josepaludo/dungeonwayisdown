from random import choice, random
from time import sleep


class Living():

    def __init__(self):

        self.x = None
        self.y = None
        self.sym = ""
        self.name = None

        self.heal_sym = 'h'
        self.invulnerable_sym = 'i'
        self.axe_sym = 'x'
        self.claw_sym = 'c'

        self.health = 20
        self.dead = False
        self.invulnerable = False
        self.can_attack = True
        self.can_move = True
        self.revive_counter = 4

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

        self.board = None

        self.cards = {}
        self.card_list = []
        self.my_cards = []
        self.weak_cards, self.medium_cards, self.strong_cards = [], [], []

    def clear_screen(self):

        self.board.print_board()
        print(f"{self.sym}'s turn.\n")

    def check_coord(self, ycor, xcor):

        if self.board.board[ycor][xcor] in self.board.invalids:
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

        up = up[:rangei] if len(up) > rangei else up
        right = right[:rangei] if len(right) > rangei else right
        down = down[:rangei] if len(down) > rangei else down
        left = left[:rangei] if len(left) > rangei else left

        return up, right, down, left

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
            print("Directions:\n\n'1' for up.\n'2' for right.\n'3' for down.\n'4' for left.\n\n'q' to quit.")

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

        print("\nInvalid input. Try again.")
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

        message = f"{self.name} died.{f' {killer} slayed it.' if killer else ''}"
        self.board.add_log(message)

        return True

    def init_cards(self):

        self.strong_cards = [card for card, info in self.cards.items() if info['level'] == 'strong']
        self.medium_cards = [card for card, info in self.cards.items() if info['level'] == 'medium']
        self.weak_cards = [card for card, info in self.cards.items() if info['level'] == 'weak']

    def get_turn_cards(self):

        chance = random()

        if chance == 0:
            message = f"{self.name} couldn't draw a card."
            self.board.add_log(message)
        elif chance < 0.5:
            self.my_cards.append(choice(self.weak_cards))
        elif chance < 0.9:
            self.my_cards.append(choice(self.medium_cards))
        else:
            self.my_cards.append(choice(self.strong_cards))

    def revive_living(self, living):

        coords = self.get_urdl_coords(self.y, self.x, 1)

        for coord in coords:

            ycor, xcor = coord[0][0], coord[0][1]

            if not self.board.board[ycor][xcor] == self.board.empty_square:
                continue

            self.board.board[ycor][xcor] = living.sym
            living.dead = False
            living.y, living.x = ycor, xcor
            living.health = 15

            message = f"{self.name} revived {living.name}."
            self.board.add_log(message)

            return True

    def set_target(self, is_enemy=True):

        if self.target_counter < self.max_target_counter:

            self.target_counter += 1
            return

        livings = self.board.allies if is_enemy else self.board.enemies
        targets = [living for living in livings if not living.dead]

        self.target = choice(targets)
        self.target_counter = 0

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

    def turn_move(self):

        self.set_target()
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

        self.dead = True
        report = f"{self.name} fell on a hole and died."
        self.board.add_log(report)

    def living_maintance(self):

        for i in range(self.actions_per_turn):
            self.get_turn_cards()

        self.actions = max(self.actions, self.actions_per_turn)
        self.moves = max(self.moves, self.moves_per_turn)

    def summon_enemy_ally(self, summon_class, is_enemy=True):

        coords = self.get_urdl_coords(self.y, self.x, 1)

        for coord in coords:

            ycor, xcor = coord[0][0], coord[0][1]

            if not self.board.board[ycor][xcor] == self.board.empty_square:
                return

            self.do_summon_enemy_ally(summon_class, ycor, xcor, is_enemy)

            return

    def do_summon_enemy_ally(self, summon_class, ycor, xcor, is_enemy):

        summon = summon_class()
        summon.y, summon.x = ycor, xcor
        summon.board = self.board

        self.board.board[ycor][xcor] = summon.sym
        self.board.livings.append(summon)

        group = self.board.enemies if is_enemy else self.board.allies
        group.append(summon)

        message = f"{self.name} summoned {summon.name}."
        self.board.add_log(message)


class Enemy(Living):

    def __init__(self):
        super().__init__()

        self.player_or_enemy = 'Enemy'

        self.sym = "e"
        self.name = "Generic small enemy"

        self.max_target_counter = 5
        self.target_counter = self.max_target_counter

