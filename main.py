from random import randint
from time import sleep
from copy import deepcopy

from board_class import Board
from living_classes import Thing, Living, Enemy
from player_class import Player
from functions import create_enemies, create_players, get_entry, game_icon


board = Board()


def dungeon_loop(board):

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


dungeon_loop(board)
