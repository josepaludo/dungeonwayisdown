from random import random, choice, randint

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

        jump = "Gains an extra move."

        self.cards = {"Jump": {"func": self.jump_func, "descr": jump, "level": "weak"}}

        self.max_health = 20
        self.max_hand_size, self.draws_per_turn = 6, 2
        self.moves, self.moves_per_turn = 2, 2
        self.actions, self.actions_per_turn = 2, 2

        self.my_cards = []
        self.weak_cards, self.medium_cards, self.strong_cards = [], [], []

    def jump_func(self):

        for key, value in self.cards.items():
            print(key, value)
        input()

    def init_cards(self):

        self.strong_cards = [card for card, info in self.cards.items() if info['level'] == 'strong']
        self.medium_cards = [card for card, info in self.cards.items() if info['level'] == 'medium']
        self.weak_cards = [card for card, info in self.cards.items() if info['level'] == 'weak']

    def get_turn_cards(self):

        chance = random()

        if chance == 0:
            pass
        elif chance < 0.3:
            self.my_cards += [choice(self.weak_cards) for i in range(2)]
        elif chance < 0.6:
            self.my_cards += [choice(self.weak_cards), choice(self.medium_cards)]
        elif chance < 0.75:
            self.my_cards += [choice(self.medium_cards) for i in range(2)]
        elif chance < 0.9:
            self.my_cards += [choice(self.strong_cards), choice(self.weak_cards)]
        elif chance < 0.98:
            self.my_cards += [choice(self.strong_cards), choice(self.medium_cards)]
        else:
            self.my_cards += [choice(self.strong_cards) for i in range(2)]

    def maintance(self, board, enemies, players):

        self.get_info(board, enemies, players)

        self.actions = self.actions_per_turn if self.actions < self.actions_per_turn else self.actions
        self.moves = self.moves_per_turn if self.moves < self.moves_per_turn else self.moves

        for i in range(self.draws_per_turn):
            self.get_turn_cards()

        self.discard_excess_cards()

    def discard_excess_cards(self):

        excess_cards = len(self.my_cards)-self.max_hand_size
        for x in range(excess_cards):

            if x == 0:
                self.clear_screen()
                print(f"\nYou've reached the maximum hand size of {self.max_hand_size}.")
                print(f"{excess_cards} random card{'s ' if excess_cards>1 else ' '}will be discarted.\n")
                input(f"Press 'Enter' to return.")
                self.clear_screen()

            random_card_index = randint(0, len(self.my_cards)-1)
            self.my_cards.pop(random_card_index)

    def help(self):

        self.clear_screen()

        print("These are the valid inputs:")
        print("(Note you must enter only what is inside the '')\n")

        for key in self.inputs:
            print(f"'{key}': {self.inputs[key][1]}")

    def more_help(self):

        print("\nMore help here.")

    def show_icons(self):

        self.board.print_board()
        print(f"W: Warrior, player.\nD: Druid, player.\nZ: Wizard, player.\nT: Thief, player\nP: Priest, player"
              f"\n{self.board.wall_square}: wall.\n{self.board.hole_square}: hole in the ground."
              f"\ne: generic small enemy.\nE: Generic large enemy.\nB: Boss.\nb: boss summons.\n")

    def show_status(self):

        self.clear_screen()

        for companion in self.companions:

            if companion.dead:
                print(f"{companion.sym} is dead.")
            else:
                print(f"{companion.sym} health is {companion.health}/{companion.max_health}.")

    def show_cards(self):

        self.clear_screen()

        for card in set(self.my_cards):
            print(f"\nCard name: {card}.\nDescription: {self.cards[card]['descr']}")

    def show_log(self):

        self.clear_screen()
        print("Log of last events:\n")

        for log in self.board.log:
            print(log)

    def move(self):

        if self.moves > 0:
            self.move_input()
        else:
            print("\nNot enough moves.")
            input("\nPress 'Enter' to return.")

    def move_input(self):

        self.clear_screen()

        while True:

            di = input("Which direction?\n'1' for up\n'2' for right\n'3' for down\n'4' for left\n'q' for quit\n: ")

            if di == 'q':
                return

            try:
                di = int(di)
                xcor = self.x-1 if di == 4 else self.x+1 if di == 2 else self.x
                ycor = self.y-1 if di == 1 else self.y+1 if di == 3 else self.y
                to = self.board.board[ycor][xcor]
            except (ValueError, IndexError):
                pass
            else:

                if 0 < di < 5:
                    if to == self.board.empty_square or to == self.board.hole_square:
                        break

            print("\nEnter a valid input.\n")

        self.make_movement(ycor, xcor)

    def make_movement(self, ycor, xcor):

        self.moves -= 1

        self.board.make_copy()

        if not self.board.board[ycor][xcor] == self.board.hole_square:
            self.board.board[ycor][xcor] = self.sym
        else:
            self.dead = True

        self.board.board[self.y][self.x] = self.board.empty_square
        self.x, self.y = xcor, ycor
        self.blink_screen()
        self.board.empty_copy()

    def action(self):

        if self.actions < 1:
            print("\nNot enough actions.")
            input("\nPress 'Enter' to return")
            return

        self.clear_screen()
        self.print_options()

        action = self.action_input()

        if not action:
            return

        self.make_action(action)

    def make_action(self, action):

        self.board.make_copy()
        func = self.cards[action]["func"]()

        if func:
            self.actions -= 1
            self.my_cards.remove(action)
            self.blink_screen()

        self.board.empty_copy()

    def print_options(self):

        print("Your cards:", end='')
        for ind, card in enumerate(self.my_cards):
            print(f" {card}{'.' if ind==len(self.my_cards)-1 else ','}", end='')

        print("\n")
        for ind, card in enumerate(self.my_cards):
            print(f"Enter '{ind+1}' for '{card}'.")

        print("Enter 'q' to quit.")

    def test_input(self, act_input):

        try:
            act_input = int(act_input)
        except (TypeError, ValueError):
            return
        else:
            act_input -= 1
            if 0 <= act_input < len(self.my_cards):
                return self.my_cards[act_input]

    def action_input(self):

        while True:

            act_input = input("\nWhich card do you want to use? ")

            if act_input == 'q':
                return

            test = self.test_input(act_input)
            if test:
                return test

            input("\nEnter a valid input.\n\nPress 'Enter' to return.")
