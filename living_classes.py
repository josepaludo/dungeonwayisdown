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
        """you must deal with proxy yourself!!!"""

        for i in range(5):
            sleep(0.05)
            self.board.print_board(self.board.backup_board)
            sleep(0.05)
            self.board.print_board()


    def get_info(self, board, enemies, players):

        self.board = board
        self.enemies = enemies
        self.companions = players


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

