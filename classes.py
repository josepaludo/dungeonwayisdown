import os


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
        self.reset_board()

    def reset_board(self):

        self.board = [[self.empty_square for i in range(20)] for j in range(20)]
        self.board[0] = self.board[-1] = ["X" for i in range(20)]
        for line in self.board:
            line[0] = line[-1] = "X"


    def print_board(self):

        os.system('cls' if os.name == 'nt' else 'clear')

        print()
        for line in self.board:
            print(" ", end='')
            for symbol in line:
                print(f"{symbol} ", end='')
            print(".")
        print()


    def place_things(self, array_of_things):

        self.reset_board()

        for thing in array_of_things:
            if isinstance(thing.x, int):
                self.board[thing.y][thing.x] = thing.sym
            else:
                for xcor in thing.x:
                    for ycor in thing.y:
                        self.board[ycor][xcor] = thing.sym


