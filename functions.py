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

        go_on = living_turn(livings, board, players, enemies)

        if not go_on:
            break


def living_turn(livings, board, players, enemies):

    while True:

        if all_players_died(players):
            return

        for living in livings:

            board.print_board()

            if board.level_finished(players, enemies):
                return True

            if not living.dead:

                if isinstance(living, Enemy):
                    enemy_turn(living, board, players, enemies)

                else:
                    player_turn(living, board, players, enemies)


def enemy_turn(living, board, players, enemies):

    board.make_copy()
    living.take_turn(players)
    blink_screen(board)
    board.backup_board = []


def blink_screen(board):
    """you must deal with proxy yourself!!!"""

    for i in range(2):
        sleep(0.05)
        board.print_board(board.backup_board)
        sleep(0.05)
        board.print_board()


def player_turn(living, board, players, enemies):

    living.get_info(board, players)

    while True:
        action = input("Which action would you like to take? ")
        if action in living.inputs:
            break
    living.inputs[action]()


def all_players_died(players):

    for player in players:
        if not player.dead:
            return False
    return True
