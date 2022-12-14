import os
from random import randint, choice

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
        self.board = []
        self.start = 0
        self.reset_board()

    def reset_board(self):

        self.board = [[self.empty_square for i in range(20)] for j in range(20)]
        self.board[0] = ["X" for i in range(20)]
        self.board[-1] = ["X" for i in range(20)]

        for line in self.board:
            line[0] = line[-1] = "X"


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


    def place_things(self, array_of_things, entry):

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

    def make_entrance(self, entry=1, determined_start=None):

        start = determined_start if determined_start else randint(2, 13)
        self.start = start

        if entry%2 != 0:
            for i in range(5):
                self.board[0 if entry == 1 else -1][start+i] = self.empty_square

        else:
            for ind, line in enumerate(self.board):
                if start<=ind<start+5:
                    line[0 if entry == 4 else -1] = self.empty_square


    def pillars_prototype(self, xcor=None, ycor=None):


        xcor = xcor if xcor else randint(5, 12)
        ycor = ycor if ycor else randint(5, 12)

        for i in range(9):
            for j in range(9):
                if self.board[ycor-3+i][xcor-3+j] != self.empty_square:
                    return

        for i in range(3):
            for j in range(3):
                self.board[ycor+i][xcor+j] = "X"


    def make_pillars(self):

        for j in range(80):
            if self.pillars_prototype():
                break


    def make_exit(self, entry=3, determined_start=None):

        self.make_entrance(choice([x for x in [1, 2, 3, 4] if x != entry]))
