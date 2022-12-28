import os
from random import randint, choice
from copy import deepcopy
from time import sleep


class Board:

    def __init__(self):

        self.empty_square = " "
        self.wall_square = "#"
        self.hole_square = "-"
        self.invalids = [self.wall_square, self.hole_square]

        self.board = []
        self.backup_board = []

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

        self.reset_board()

    def board_blink(self):

        for i in range(5):

            sleep(0.05)
            self.print_board(self.backup_board)
            sleep(0.05)
            self.print_board()

    def livings_maintance(self, livings, enemies, allies, players):

        self.livings += livings
        self.enemies += enemies
        self.allies += allies
        self.players += players

    def clear_livings(self):

        self.livings, self.enemies = [], []
        self.allies, self.players = [], []

    def add_log(self, log):

        self.log.append(log)

        if len(self.log) > 10:
            self.log.pop(0)

    def level_finished(self):

        for player in self.players:

            if player.dead:
                continue

            if (player.x, player.y) not in self.exit_coords:
                return

        for enemy in self.enemies:

            if not enemy.dead:
                return

        return True

    def check_dead_players(self):

        for player in self.players:

            if player.dead:
                self.dead_players.append(player.sym)

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
