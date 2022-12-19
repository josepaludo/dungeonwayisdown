from random import choice
from time import sleep


class Thing:

    def __init__(self):

        self.x = None
        self.y = None
        self.sym = ""


class Living(Thing):

    def __init__(self):
        super().__init__()

        self.health = 20
        self.weapons = []
        self.abilities = []
        self.dead = False
        self.name = None

        self.board = None
        self.enemies = None
        self.companions = None

    def clear_screen(self):

        self.board.print_board()
        print(f"{self.sym}'s turn.\n")

    def blink_screen(self):

        for i in range(5):
            sleep(0.05)
            self.board.print_board(self.board.backup_board)
            sleep(0.05)
            self.board.print_board()

    def get_info(self, board, enemies, players):

        self.board = board
        self.enemies = enemies
        self.companions = players

    def check_coord(self, ycor, xcor):
        """returns tuple with coord object, class name, symbol"""

        for living in self.enemies + self.companions:
            if (living.y, living.x) == (ycor, xcor):
                return living, living.__class__.name, living.sym

        invalid_locs = [self.board.empty_square, self.board.hole_square, self.board.wall_square]

        for invalid_loc in invalid_locs:
            if self.board.board[ycor][xcor] == invalid_loc:
                return None, None, invalid_loc

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

    def prompt_for_direction(self):

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

    def check_if_dead(self, killer=None):

        if self.health > 0:
            return

        self.dead = True
        self.board.board[self.y][self.x] = self.board.empty_square

        mess = f"{self.name} died.{f' {killer} slayed it.' if killer else ''}"
        self.board.add_log(mess)

        return True


class Enemy(Living):

    def __init__(self, board):
        super().__init__()

        self.sym = "e"
        self.name = "Generic small enemy"
        self.targets = None
        self.target = None
        self.current_diff = None
        self.dir = []
        self.board = board
        self.max_target_counter = 15
        self.target_counter = self.max_target_counter

    def set_target(self):

        if self.target_counter >= self.max_target_counter:
            self.target = choice(self.targets)
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

        self.measure_distance()

        if self.current_diff == 1:
            return

        for direc in self.dir:

            boardxy = self.board.board[direc[0]][direc[1]]
            if boardxy == self.board.empty_square or boardxy == self.board.hole_square:

                if self.dist(direc) < self.current_diff:
                    self.board.board[self.y][self.x] = self.board.empty_square

                    if boardxy == self.board.hole_square:
                        self.dead = True
                        report = "Enemy fell on a hole and died."
                        self.board.add_log(report)
                        return

                    self.y, self.x = direc[0], direc[1]
                    self.board.board[self.y][self.x] = self.sym
                    return

    def turn_move(self, targets):

        self.targets = [target for target in targets if not target.dead]
        self.set_target()
        self.move()
