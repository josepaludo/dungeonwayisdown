from random import randint
from copy import deepcopy
from time import sleep

from player_class import Player, Warrior, Druid, Thief, Wizard, Priest
from living_classes import Enemy
from board_class import Board


def create_enemies(Clas, board):

    num_min = randint(3, 6)
    num_max = num_min+(randint(1, 5))

    proxy = []

    for i in range(randint(num_min, num_max)):

        geni = Clas(board)
        proxy.append(geni)

    return proxy


def create_players():

    proxy_list = []
    for class_ in [Warrior, Druid, Thief, Wizard, Priest]:
        proxy = class_()
        proxy_list.append(proxy)

    return proxy_list


def dungeon_loop():

    board = Board()

    while True:

        players = create_players()
        enemies = create_enemies(Enemy, board)
        livings = enemies + players
        board.place_things(enemies, players)

        living_turn(livings, board, players, enemies)


def living_turn(livings, board, players, enemies):

    while True:
        for living in livings:

            board.print_board()

            if isinstance(living, Enemy):

                enemy_turn(living, board, players, enemies)


            if isinstance(living, Player):

                player_turn(living, board, players, enemies)


def enemy_turn(living, board, players, enemies):

    board.backup_board = deepcopy(board.board)

    living.take_turn(players)

    for i in range(2):
        sleep(0.05)
        board.print_board(board.backup_board)
        sleep(0.05)
        board.print_board()

    board.backup_board = []


def player_turn(living, board, players, enemies):

    while True:
        action = input("Which action would you like to take? ")
        if action in living.inputs:
            break
    living.inputs[action]()
    sleep(5)


game_icon = """
______
|  _  |
| | | |_   _ _ __   __ _  ___  ___  _ __
| | | | | | | '_ \ / _` |/ _ \/ _ \| '_  |
| |/ /| |_| | | | | (_| |  __/ (_) | | | |
|___/  \__,_|_| |_|\__, |\___|\___/|_| |_|
                    __/ |
                   |___/
    _    _
   | |  | |
   | |  | | __ _ _   _
   | |/\| |/ _` | | | |
   \  /\  / (_| | |_| |
    \/  \/ \__,_|\__, |
                  __/ |
                 |___/
  _      ______
 (_)     |  _  |
  _ ___  | | | |_____      ___ __
 | / __| | | | / _ \ \ /\ / / '_  |
 | \__ \ | |/ / (_) \ V  V /| | | |
 |_|___/ |___/ \___/ \_/\_/ |_| |_|
\n"""
