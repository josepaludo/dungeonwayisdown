from random import choice, random
from time import sleep


class Living():

    def __init__(self):

        self.x = None
        self.y = None
        self.sym = ""

        self.heal_sym = 'h'
        self.invulnerable_sym = 'i'
        self.axe_sym = 'x'

        self.health = 20
        self.weapons = []
        self.abilities = []
        self.dead = False
        self.name = None

        self.invulnerable = False
        self.can_attack = True

        self.board = None

        self.cards = {}
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


class Enemy(Living):

    def __init__(self):
        super().__init__()

        self.player_or_enemy = 'Enemy'

        self.sym = "e"
        self.name = "Generic small enemy"

        self.target = None
        self.current_diff = None
        self.dir = []
        self.max_target_counter = 15
        self.target_counter = self.max_target_counter

        self.moves = 1
        self.moves_per_turn = 1

        self.actions = 1
        self.actions_per_turn = 1

        self.card_list = []
        self.my_cards = []

    def enemy_maintance(self):

        for i in range(self.actions_per_turn):
            self.get_turn_cards()

        self.actions = max(self.actions, self.actions_per_turn)
        self.moves = max(self.moves, self.moves_per_turn)

    def empty_hand(self):

        self.my_cards = []

    def set_target(self):

        if self.target_counter >= self.max_target_counter:
            targets = [ally for ally in self.board.allies if not ally.dead]
            self.target = choice(targets)
            self.target_counter = 0

        else:
            self.target_counter += 1

    def measure_distance(self):

        xdiff, ydiff = abs(self.target.x-self.x), abs(self.target.y-self.y)
        self.current_diff = xdiff+ydiff

        up, down = (self.y-1, self.x), (self.y+1, self.x)
        left, right = (self.y, self.x-1), (self.y, self.x+1)

        self.dir = up, right, down, left

    def dist(self, coor):

        xdiff = abs(coor[1]-self.target.x)
        ydiff = abs(coor[0]-self.target.y)

        return xdiff+ydiff

    def move(self):

        if self.current_diff == 1:
            return

        for direction in self.dir:

            if self.try_to_move(direction):
                return

    def try_to_move(self, direc):

        boardxy = self.board.board[direc[0]][direc[1]]
        if boardxy not in [self.board.empty_square, self.board.hole_square]:
            return

        if self.dist(direc) < self.current_diff:
            self.make_the_move(direc, boardxy)
            return True

    def make_the_move(self, direc, boardxy):

        self.board.board[self.y][self.x] = self.board.empty_square

        if boardxy == self.board.hole_square:
            self.hole_fall()
            return

        self.y, self.x = direc[0], direc[1]
        self.board.board[self.y][self.x] = self.sym

    def hole_fall(self):

        self.dead = True
        report = "Enemy fell on a hole and died."
        self.board.add_log(report)

    def turn_move(self):

        self.set_target()
        self.measure_distance()
        self.move()

