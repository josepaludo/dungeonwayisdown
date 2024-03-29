import csv
from random import randint, choice

from src.Living import Living


class Ally(Living):

    def __init__(self):
        super().__init__()

        self.player_or_enemy = 'Ally'

        self.target = None
        self.max_target_counter = 5
        self.target_counter = self.max_target_counter
        self.current_diff = None

        self.moves_per_turn = 1
        self.moves = self.moves_per_turn

        self.actions_per_turn = 1
        self.actions = self.actions_per_turn

        self.card_list = []
        self.my_cards = []


class Player(Living):

    def __init__(self):
        super().__init__()

        self.player_or_enemy = 'Player'

        self.inputs = {"move": {"func": self.move,
                                "descr": "Move up, down, left or right."},
                       "act": {"func": self.action,
                               "descr": "Use one of your cards."},
                       "log": {"func": self.show_log,
                               "descr": "Shows log of last important events."},
                       "cards": {"func": self.show_cards,
                                 "descr": "Shows every card you have "
                                 "and how it works."},
                       "status": {"func": self.show_status,
                                  "descr": "Shows status of each player."},
                       "icons": {"func": self.show_icons,
                                 "descr": "Shows the meaning of each icon."},
                       "help": {"func": self.help,
                                "descr": "Shows every possible input."},
                       "mhelp": {"func": self.more_help,
                                 "descr": "Gives more help."},
                       "end": {"func": "",
                               "descr": "Finish your turn."},
                       "dragons": {"func": self.dragons,
                                   "descr": ""}}

        self.max_health = 20
        self.max_hand_size, self.draws_per_turn = 6, 2
        self.moves, self.moves_per_turn = 2, 2
        self.actions, self.actions_per_turn = 2, 2

        self.cards = {}

        self.get_player_cards()

    def get_player_cards(self):

        jump = "Gains an extra move."
        self.cards["Jump"] = {"func": self.jump_func,
                              "descr": jump,
                              "level": "weak"}

    def dragons(self):

        self.clear_screen()

        print(choice(self.board.quotes))

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

        return True

    def player_maintenance(self):

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
                print(f"\nYou've reached the maximum hand size of "
                      f"{self.max_hand_size}.")
                print(f"{excess_cards} random card"
                      f"{'s ' if excess_cards > 1 else ' '}will be discarted.")
                input(f"\nPress 'Enter' to return.")
                self.clear_screen()

            random_card_index = randint(0, len(self.my_cards)-1)
            self.my_cards.pop(random_card_index)

    def help(self):

        self.clear_screen()

        print("These are the valid inputs:")
        print("(Note you must enter only what is inside the '')\n")

        for key in self.inputs:

            if key == "dragons":
                continue

            print(f"'{key}': {self.inputs[key]['descr']}")

    def more_help(self):

        self.clear_screen()
        print("More help:\n\nget good")

    def show_icons(self):

        self.board.print_board()

        print("Livings' Symbols:\n")

        for living in self.board.livings:
            print(f"  {living.sym}: {living.name}, {living.player_or_enemy}.")

        print("\nOther Symbols:\n")

        self.print_other_icons()

    def print_other_icons(self):

        with open("src/assets/icons.csv") as file:
            file = csv.reader(file)

            for index, line in enumerate(file):
                for ind, entry in enumerate(line):

                    icon_message = f"  {entry}:" if ind == 0 else f" {entry}."
                    print(icon_message, end="")

                print()

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
            print(f"\nCard name: {card}.\n"
                  f"Description: {self.cards[card]['descr']}")

    def show_log(self):

        self.clear_screen()
        print("Log of last events:")

        for ind, log in enumerate(reversed(self.board.log)):

            turn = 'Current turn' if ind == 0 else 'Last turn' if ind == 1 \
                   else 'The turn before'
            print(f"\n{turn}:\n")

            for entry in log:
                print(f"    {entry}")

        print()

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

        di = input("Which direction?\n'1' for up\n'2' for right\n"
                   "'3' for down\n'4' for left\n'q' for quit\n: ")

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

            if not (0 < di < 5):
                return

            if to in [self.board.empty_square, self.board.hole_square]:
                return ycor, xcor

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

            self.clear_screen()
            self.print_options()

            act_input = input("\nWhich card do you want to use? ")
            if act_input == 'q':
                return

            test = self.test_input(act_input)
            if test:
                return test

            self.wrong_input_warning()

    def player_urdl_damage(self, reach, sym, damage, message):

        valid_side = self.prompt_direction()

        if not valid_side:
            return

        directions = self.get_urdl_coords(self.y, self.x, reach)[valid_side-1]

        for direction in directions:
            for coord in direction:

                self.do_player_damage(coord, sym, damage, message)

        return True

    def player_around_damage(self, reach, sym, damage, message, question,
                             func=None, arg=None):

        go_on = self.yes_no_input(question)

        if not go_on:
            return

        coords = self.get_around_coords(self.y, self.x, reach)

        for coord in coords:

            self.do_player_damage(coord, sym, damage, message, func, arg)

        return True

    def do_player_damage(self, coord, sym, damage, message,
                         func=None, arg=None):

        ycor, xcor = coord[0], coord[1]
        target = self.check_coord(ycor, xcor)

        if target == "invalid":
            return

        self.board.backup_board[ycor][xcor] = sym

        if target not in self.board.enemies:
            return

        target.health -= damage

        if func:
            func(target, arg)

        message = message.split("#")
        message = message[0] + target.name + message[1]
        self.board.add_log(message)

        target.check_if_dead(self)

        return target

    def find_enemy_in_line(self, sym, damage, message):

        direction = self.prompt_direction()

        if not direction:
            return

        coords = self.get_urdl_coords_all(self.y, self.x)[direction-1]

        for coord in coords:

            target = self.do_player_damage(coord, sym, damage, message)

            if not target:
                continue

            return target

    def damage_around_enemies(self, reach, sym, damage, message):

        for enemy in self.board.enemies:

            coords = self.get_around_coords(enemy.y, enemy.x, reach, False)

            for coord in coords:

                self.do_player_damage(coord, sym, damage, message)

    def fill_line_until_hit(self, direction, sym, damage, message):

        for coord in direction:

            if self.check_coord(coord[0], coord[1]) == 'invalid':
                return

            target = self.do_player_damage(coord, sym, damage, message)

            if target:
                return target

