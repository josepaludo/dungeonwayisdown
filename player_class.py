from copy import deepcopy
from time import sleep

from living_classes import Living

class Player(Living):

    def __init__(self):
        super().__init__()

        self.inputs = {"move": self.move}

                       #"log": self.log,
                       #"cards": self.cards,
                       #"status": self.status,
                       #"weapons": self.weapons,
                       #"icons": self.weapons,
                       #"more help": self.more_help,
                       #"move": self.move}


    def move(self):

        while True:

            di = input("Which direction?\n'1' for up\n'2' for right\n'3' for down\n'4' for left\n'q' for quit\n: ")

            if di == 'q':
                return

            try:
                di = int(di)
                xcor = self.x-1 if di==4 else self.x+1 if di==2 else self.x
                ycor = self.y-1 if di==1 else self.y+1 if di==3 else self.y
                to = self.board.board[ycor][xcor]
            except (ValueError, IndexError):
                pass
            else:

                if 0<di<5:
                    if to == self.board.empty_square or to == self.board.hole_square:
                        break

            print("Enter a valid input.")

        self.make_movement(ycor, xcor)


    def make_movement(self, ycor, xcor):

        self.board.make_copy()

        if not self.board.board[ycor][xcor] == self.board.hole_square:
            self.board.board[ycor][xcor] = self.sym
        else:
            self.dead = True

        self.board.board[self.y][self.x] = self.board.empty_square
        self.x, self.y = xcor, ycor
        self.blink_screen()
        self.backup_board = []


class Warrior(Player):

    def __init__(self):
        super().__init__()

        self.sym = "W"
        self.inputs["attack"] = "aaa"

class Priest(Player):

    def __init__(self):
        super().__init__()

        self.sym = "P"


class Druid(Player):

    def __init__(self):
        super().__init__()

        self.sym = "D"


class Wizard(Player):

    def __init__(self):
        super().__init__()

        self.sym = "Z"


class Thief(Player):

    def __init__(self):
        super().__init__()

        self.sym = "T"

