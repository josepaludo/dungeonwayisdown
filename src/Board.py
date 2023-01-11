import os
from random import randint, choice
from copy import deepcopy
from time import sleep

from src.Constants import GAME_ICON


class Board:

    def __init__(self):

        self.empty_square = " "
        self.wall_square = "#"
        self.hole_square = "-"
        self.invalids = [self.wall_square, self.hole_square]

        self.available_names = []
        self.boss_epithets = []

        self.board = []
        self.backup_board = []

        self.level = 0

        self.exit = 0
        self.next_entry = 3
        self.entry = 0
        self.start = 7
        self.entrance_coords = []
        self.exit_coords = []

        self.log = []
        self.living_turn_checker = []
        self.dungeon_loop_checker = []
        self.dead_players = []

        self.livings = []
        self.enemies = []
        self.allies = []
        self.players = []

        self.quotes = []
        self.player_names = []

        self.reset_board()
        self.init_quotes()

    def init_quotes(self):

        with open("src/assets/quotes.txt") as file:

            file = file.read().split("#")

            for ind, quote in enumerate(file):

                if ind == len(file)-1:
                    continue

                self.quotes.append(quote)

    def pick_boss_epithet(self):

        if len(self.boss_epithets) == 0:
            self.set_boss_names()

        epithet_index = randint(0, len(self.boss_epithets)-1)
        epithet = self.boss_epithets.pop(epithet_index)

        return epithet

    def set_boss_names(self):

        self.boss_epithets = ["Epic", "Magnificent", "Glorious", "Majestic",
                              "Imposing", "Monumental", "Massive", "Grand",
                              "Royal", "Proud", "Colossal", "Lavish", "Huge"]

    def set_names(self):

        with open("src/assets/names.txt") as file:

            file = file.readlines()[0].split(',')
            file.pop(-1)

            self.available_names = file

    def pick_name(self):

        if len(self.available_names) == 0:
            self.set_names()

        name_index = randint(0, len(self.available_names)-1)
        name = self.available_names.pop(name_index)

        return name

    def set_player_names(self):

        with open("src/assets/player_names.txt") as file:

            names = file.read().split("#")
            names.pop(-1)

            self.player_names = names

    def pick_player_name(self):

        if len(self.player_names) == 0:
            self.set_player_names()

        name_index = randint(0, len(self.player_names)-1)
        name = self.player_names.pop(name_index)

        return name

    def print_backup_board(self):

        self.print_board(self.backup_board)

    def board_blink(self):

        for i in range(5):

            sleep(0.1)
            self.print_backup_board()
            sleep(0.1)
            self.print_board()

    def livings_maintenance(self, livings, enemies, allies, players):

        self.livings += livings
        self.enemies += enemies
        self.allies += allies
        self.players += players

    def clear_livings(self):

        self.livings, self.enemies = [], []
        self.allies, self.players = [], []

    def erase_log(self):

        self.log = []

    def erase_turn_checker(self):

        self.living_turn_checker = []

    def log_maintenance(self):

        self.log.append([])

        if len(self.log) > 3:
            self.log.pop(0)

    def add_log(self, log):

        self.log[-1].append(log)

    def level_finished(self):

        for player in self.players:

            if player.dead:
                continue

            if (player.x, player.y) not in self.exit_coords:
                return

        for enemy in self.enemies:

            if not enemy.dead:
                return

        self.level_finished_warning()

        return True

    def level_finished_warning(self):

        self.print_game_icon()

        message = "Your party has reached the final level of the dungeon.\n\n"\
                  "Press 'Enter' to continue."

        input(f"Your party has finished the level {self.level}.\n\n"
              f"\nPress 'Enter' do advance to follow the dungeon way."
              if self.level < 10 else message)

    def check_dead_players(self):

        for player in self.players:

            if player.dead:
                self.dead_players.append(player.sym)

    def game_finished(self):

        self.level += 1

        if self.level == 11:
            return True

    def make_copy(self):

        self.backup_board = deepcopy(self.board)

    def empty_copy(self):

        self.backup_board = []

    def reset_board(self):

        self.board = [[self.empty_square for i in range(20)] for j in range(20)]

        self.board[0] = [self.wall_square for i in self.board[0]]
        self.board[-1] = [self.wall_square for i in self.board[-1]]

        for line in self.board:
            line[0] = line[-1] = self.wall_square

    def clean_clear(self):

        os.system('cls' if os.name == 'nt' else 'clear')

    def print_game_icon(self):

        self.clean_clear()
        print(GAME_ICON)

    def print_board(self, proxy_board=None):

        proxy_board = proxy_board if proxy_board else self.board

        self.clean_clear()

        print()
        for line in proxy_board:
            print(" ", end='')
            for symbol in line:
                print(f"{symbol} ", end='')
            print()
        print()

    def place_things(self):

        self.entry = self.next_entry

        self.reset_board()

        self.make_entrance()
        self.make_exit()
        self.make_pillars()
        self.make_holes()

        self.place_players()
        self.place_enemies()

    def place_enemies(self):

        for enemy in self.enemies:

            self.set_enemy_xy(enemy)
            self.board[enemy.y][enemy.x] = enemy.sym

    def set_enemy_xy(self, enemy):

        is_entry_up_down = self.entry % 2 != 0
        is_entry_right = self.entry == 2
        is_entry_down = self.entry == 3

        xrange = (1, 18) if is_entry_up_down else (1, 9) if is_entry_right else (10, 18)
        yrange = (1, 18) if not is_entry_up_down else (1, 9) if is_entry_down else (10, 18)

        while True:

            xpos = randint(xrange[0], xrange[1])
            ypos = randint(yrange[0], yrange[1])

            if self.board[ypos][xpos] == self.empty_square:
                enemy.x, enemy.y = xpos, ypos
                break

    def place_players(self):

        for coord, player in zip(self.entrance_coords, self.players):
            player.x = coord[0]
            player.y = coord[1]
            self.board[player.y][player.x] = player.sym

    def make_entrance(self, entry=None, is_entrance=True):

        start = self.entrance_start(is_entrance)
        entry = entry if entry else self.entry
        is_up_or_down = entry % 2 != 0

        if is_up_or_down:
            self.make_up_down_entrance(start, entry, is_entrance)
        else:
            self.make_left_right_entrance(start, entry, is_entrance)

    def entrance_start(self, is_entrance):

        if is_entrance:
            self.entrance_coords = []
            start = self.start

        else:
            start = randint(3, 12)
            self.start = start
            self.exit_coords = []

        return start

    def make_up_down_entrance(self, start, entry, is_entrance):

        y = 0 if entry == 1 else 19

        for i in range(5):

            x = start+i
            self.board[y][x] = self.empty_square
            self.add_coords(x, y, is_entrance)

    def make_left_right_entrance(self, start, entry, is_entrance):

        x = 0 if entry == 4 else 19

        for ind, line in enumerate(self.board):

            if start <= ind < start+5:
                y = ind
                line[x] = self.empty_square
                self.add_coords(x, y, is_entrance)

    def add_coords(self, x, y, entrance=True):

        if entrance:
            self.entrance_coords.append((x, y))
        else:
            self.exit_coords.append((x, y))

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

        self.exit = choice([x for x in [1, 2, 3, 4] if x != self.entry])
        self.make_entrance(self.exit, is_entrance=False)
        self.next_entry = 1 if self.exit == 3 else 2 if self.exit == 4 else 3 if self.exit == 1 else 4

    def make_holes(self):

        size = randint(2, 3)
        check = 4
        for j in range(25):
            self.pillars_prototype(size=size, check=size+check, subtract=check//2, wall=False)
