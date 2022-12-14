import os
from random import randint, choice
from copy import deepcopy

from functions import get_entry


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

    def __init__(self):
        super().__init__()


    def move(self):
        pass


class Board:

    def __init__(self):

        self.empty_square = " "
        self.wall_square = "#"
        self.hole_square = "*"
        self.board = []
        self.current_exit = 0
        self.entry = 0
        self.backup_board = []
        self.reset_board()

    def reset_board(self):

        self.board = [[self.empty_square for i in range(20)] for j in range(20)]
        self.board[0] = [self.wall_square for i in range(20)]
        self.board[-1] = [self.wall_square for i in range(20)]

        for line in self.board:
            line[0] = line[-1] = self.wall_square


    def print_board(self, proxy_board=None):

        proxy_board = proxy_board if proxy_board else self.board

        os.system('cls' if os.name == 'nt' else 'clear')

        print()
        for line in proxy_board:
            print(" ", end='')
            for symbol in line:
                print(f"{symbol} ", end='')
            print()
        print()


    def place_things(self, array_of_things, entry=3):

        entry = self.entry if self.entry != 0 else entry

        self.reset_board()

        for thing in array_of_things:
            if isinstance(thing.x, int):
                self.board[thing.y][thing.x] = thing.sym
            else:
                for xcor in thing.x:
                    for ycor in thing.y:
                        self.board[ycor][xcor] = thing.sym

        self.make_entrance(entry)
        self.make_exit(entry)
        self.make_pillars()
        self.make_holes()

        self.backup_board = deepcopy(self.board)

    def make_entrance(self, entry):

        if entry%2 != 0:
            for i in range(5):
                self.board[0 if entry == 1 else -1][start+i] = self.empty_square

        else:
            for ind, line in enumerate(self.board):
                if start<=ind<start+5:
                    line[0 if entry == 4 else -1] = self.empty_square


    def pillars_prototype(self, xcor=None, ycor=None, size=3, check=3, subtract=0, wall=True):


        xcor = xcor if xcor else randint(3, 13)
        ycor = ycor if ycor else randint(3, 13)

        for i in range(check):
            for j in range(check):
                if self.board[ycor-subtract+i][xcor-subtract+j] != self.empty_square:
                    return

        for i in range(size):
            for j in range(size):
                self.board[ycor+i][xcor+j] = self.wall_square if wall else self.hole_square


    def make_pillars(self):

        options = [(4, 4), (4, 13), (13, 4), (13, 13)]
        for opt in options:
            self.pillars_prototype(ycor=opt[0], xcor=opt[1])


    def make_exit(self, entry):

        self.current_exit = choice([x for x in [1, 2, 3, 4] if x != entry])
        self.make_entrance(self.current_exit)


    def make_holes(self, xcor=None, ycor=None):

        h_size = randint(2, 3)
        for j in range(25):
            self.pillars_prototype(size=h_size, check=h_size+4, subtract=2, wall=False, wall_distance=2)
