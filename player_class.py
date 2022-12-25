from random import random, choice, randint

from living_classes import Living, Enemy


class Ally(Living):

    def __init__(self, board):
        super().__init__()

        self.player_or_enemy = 'Ally'
        self.board = board

        self.append_to_board_allies()

    def append_to_board_allies(self):

        if self in self.board.allies:
            return

        self.board.allies.append(self)


class Player(Living):

    def __init__(self):
        super().__init__()

        self.player_or_enemy = 'Player'

        self.inputs = {"move": {"func": self.move,
                                "descr": "Move up, down, left or right."},
                       "act": {"func": self.action,
                               "descr": "Use one of your cards."},
                       "log": {"func": self.show_log,
                               "descr": "Shows a log of last important events."},
                       "cards": {"func": self.show_cards,
                                 "descr": "Shows every card you have and how it works."},
                       "status": {"func": self.show_status,
                                  "descr": "Shows status of each player."},
                       "icons": {"func": self.show_icons,
                                 "descr": "Shows the meaning of each icon."},
                       "help": {"func": self.help,
                                "descr": "Shows every possible input."},
                       "mhelp": {"func": self.more_help,
                                 "descr": "Gives more details about the game."},
                       "end": {"func": "",
                               "descr": "Finish your turn."}}

        jump = "Gains an extra move."

        self.cards = {"Jump": {"func": self.jump_func,
                               "descr": jump,
                               "level": "weak"}}

        self.max_health = 20
        self.max_hand_size, self.draws_per_turn = 6, 2
        self.moves, self.moves_per_turn = 2, 2
        self.actions, self.actions_per_turn = 2, 2

    def append_to_turn_checker(self, func):

        if func not in self.board.living_turn_checker:
            self.board.living_turn_checker.append(func)

    def prompt_for_ally(self, question, ally_group=False):

        alive_allies = [ally for ally in self.board.allies if not ally.dead]
        ally_group = ally_group if ally_group else alive_allies

        while True:

            self.clear_screen()

            print("Choose an ally:\n")
            for ind, ally in enumerate(ally_group):
                print(f"'{ind+1}' for {ally.name}.")
            print("'q' to  quit.")

            answer = input(f"\n{question} ")

            if answer == 'q':
                return

            if not self.check_int_range(answer, 1, len(ally_group)):
                continue

            ally = ally_group[int(answer)-1]

            return ally

    def jump_func(self):

        self.moves += 1

        message = f"{self.name} jumped and can make one more move this turn"
        self.board.add_log(message)

    def player_maintance(self):

        self.actions = max(self.actions_per_turn, self.actions)
        self.moves = max(self.moves, self.moves_per_turn)

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
            print(f"'{key}': {self.inputs[key]['descr']}")

    def more_help(self):

        print("\nMore help here.")

    def show_icons(self):

        self.board.print_board()

        for living in self.board.livings:
            print(f"{living.sym}: {living.name}, {living.player_or_enemy}.")

        print(f"{self.board.wall_square}: Wall.\n{self.board.hole_square}: Hole.")

    def show_status(self):

        self.clear_screen()

        for ally in self.board.allies:

            if ally.dead:
                print(f"{ally.name} is dead.")
            else:
                print(f"{ally.name} health is {ally.health}/{ally.max_health}.")

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

        while True:

            self.clear_screen()

            result = self.prompt_for_direction()

            if result == 'q':
                return

            if result:
                ycor, xcor = result[0], result[1]
                break

            self.wrong_input_warning()

        self.make_movement(ycor, xcor)

    def prompt_for_direction(self):

        di = input("Which direction?\n'1' for up\n'2' for right\n'3' for down\n'4' for left\n'q' for quit\n: ")

        if di == 'q':
            return 'q'

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
                    return (ycor, xcor)

    def make_movement(self, ycor, xcor):

        self.moves -= 1

        self.board.make_copy()

        if not self.board.board[ycor][xcor] == self.board.hole_square:
            self.board.board[ycor][xcor] = self.sym
        else:
            self.dead = True

        self.board.board[self.y][self.x] = self.board.empty_square
        self.x, self.y = xcor, ycor
        self.board.board_blink()
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
            self.board.board_blink()

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

            self.wrong_input_warning()

