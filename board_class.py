import os
from random import randint, choice
from copy import deepcopy

from functions import get_entry


class Board:

    def __init__(self):

        self.empty_square = " "
        self.wall_square = "#"
        self.hole_square = "*"
        self.board = []
        self.exit = 0
        self.next_entry = 3
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


    def place_things(self, livings, players):

        self.entry = self.next_entry

        self.reset_board()
        self.make_entrance(players)
        self.make_exit()
        self.make_pillars()
        self.make_holes()
        self.place_livings(livings)


    def place_livings(self, livings):

        self.set_livings_xy(livings)

        for living in livings:
            if isinstance(living.x, int):
                self.board[living.y][living.x] = living.sym
            else:
                for xcor in living.x:
                    for ycor in living.y:
                        self.board[ycor][xcor] = living.sym


        self.backup_board = deepcopy(self.board)


    def set_livings_xy(self, livings):
       # entry must be 1, 2, 3, 4 standing for up, right, down, left

        for liv in livings:

            while True:
                xrange = (0, 19) if self.entry%2!=0 else (0, 9) if self.entry==2 else (10, 19)
                yrange = (0, 19) if self.entry%2==0 else (0, 9) if self.entry==3 else (10, 19)
                xpos = randint(xrange[0], xrange[1])
                ypos = randint(yrange[0], yrange[1])

                if self.board[ypos][xpos] == self.empty_square:
                    liv.x, liv.y = xpos, ypos
                    break


    def make_entrance(self, players, entry=None):

        entry = entry if entry else self.entry
        start = randint(3, 12)

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
            if randint(0, 1) == 1:
                self.pillars_prototype(ycor=opt[0], xcor=opt[1])


    def make_exit(self):

        self.exit= choice([x for x in [1, 2, 3, 4] if x != self.entry])
        self.make_entrance(self.exit)
        self.next_entry = get_entry(self.exit)


    def make_holes(self, xcor=None, ycor=None):

        size = randint(2, 3)
        check = 4
        for j in range(25):
            self.pillars_prototype(size=size, check=size+check, subtract=check//2, wall=False)
