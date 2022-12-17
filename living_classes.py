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

        self.board = None
        self.enemies = None
        self.companions = None


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

        for living in self.enemies + self.players:
            if (living.y, living.x) == (ycor, xcor):
                return living, living.__class__.name, living.sym

        invalid_locs = [self.board.empty_square, self.board.hole_square, self.board.wall_square]

        for invalid_loc in invalid_locs:
            if self.board.board[ycor][xcor] == invalid_loc:
                return None, None, invalid_loc


    def get_urdl_coords(self, ycor, xcor):

        up, down = (ycor-1, xcor), (ycor+1, xcor)
        left, right = (ycor, xcor-1), (ycor, xcor+1)

        return up, right, down, left


    def get_urdl_line_coords(self, ycor, xcor):

        up = [(ycor-i-1, xcor) for i in range(ycor)]
        down = [(ycor+i+1, xcor) for i in range(len(self.board.board)-1-ycor)]
        left = [(ycor, xcor-i-1) for i in range(xcor)]
        right = [(ycor, xcor+i+1) for i in range(len(self.board.board[0])-1-xcor)]

        return up, right, down, left


class Enemy(Living):

    def __init__(self, board):
        super().__init__()
        self.sym = "e"
        self.targets = None
        self.target = None
        self.current_diff = None
        self.dir = []
        self.board = board
        self.target_counter = 10


    def set_target(self):

        if self.target_counter == 10:
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

