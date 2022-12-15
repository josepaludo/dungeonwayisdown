from random import choice


class Thing:

    def __init__(self):

        self.x = None
        self.y = None
        self.sym = ""


class Living(Thing):

    def __init__(self):
        super().__init__()

        self.health = None
        self.weapons = []
        self.abilities = []


class Enemy(Living):

    def __init__(self, board):
        super().__init__()
        self.sym = "e"
        self.targets = None
        self.target = None
        self.current_diff = None
        self.dir = []

    def set_target(self):
        self.target = choice(self.targets)


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

            boardxy = board.board[direc[0]][direc[1]]
            if boardxy == board.empty_quare or if boardxy == board.hole_square:

                if dist(direc)<self.current_diff:
                    self.y, self.x = direc[0], direc[1]
                    board.board[self.y][self.x] = self.sym
                    return


    def take_turn(self, targets):

        self.targets = targets
