from copy import deepcopy
from time import sleep

from living_classes import Living

class Player(Living):

    def __init__(self):
        super().__init__()

        self.inputs = {"move": (self.move, "Move up, down, left or right."),
                       "act": (self.action, "Use one of your cards."),
                       "log": (self.show_log, "Shows a log of last important events."),
                       "cards": (self.show_cards, "Shows every card you have and how it works."),
                       "status": (self.show_status, "Shows status of each player."),
                       "icons": (self.show_icons, "Shows the meaning of each icon."),
                       "help": (self.help, "Shows every possible input."),
                       "mhelp": (self.more_help, "Gives more details about the game."),
                       "end": ("", "Finish your turn.")}


        self.moves = 2
        self.actions = 2
        self.cards = []
        self.max_health = 20
        self.companions = []


    def action(self):
        pass


    def clear_screen(self):

        self.board.print_board()
        print(f"{self.sym}'s turn.\n")


    def help(self):

        self.clear_screen()

        print("These are the valid inputs:")
        print("(Note you must enter only what is inside the '')\n")

        for key in self.inputs:
            print(f"'{key}': {self.inputs[key][1]}")

    def more_help(self):

        print("More help here.")


    def show_icons(self):

        self.board.print_board()
        print(f"W: Warrior, player.\nD: Druid, player.\nZ: Wizard, player.\nT: Thief, player\nP: Priest, player\n{self.board.wall_square}: wall.\n{self.board.hole_square}: hole in the ground.\ne: generic small enemy.\nE: Generic large enemy.\nB: Boss.\bb: boss summons.\n")


    def show_status(self):

        self.clear_screen()

        for companion in self.companions:

            if companion.dead:
                print(f"{companion.sym} is dead.")
            else:
                print(f"{companion.sym} health is {companion.health}/{companion.max_health}.")


    def show_cards(self):

        self.clear_screen()

        for card in self.cards:
            print(cards)


    def show_log(self):

        self.clear_screen()

        for log in self.board.log:
            print(log)


    def move(self):

        self.clear_screen()

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

            print("\nEnter a valid input.\n")

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

