from random import randint
from time import sleep
from copy import deepcopy

from board_class import Board
from living_classes import Thing, Living, Enemy
from functions import create_enemies, create_players, get_entry, game_icon


board = Board()


while True:

    enemies = create_enemies(Enemy)
    players = create_players()
    board.place_things(enemies, players)
    board.print_board()

    board.backup_board = deepcopy(board.board)
    for i in range(10):
        board.print_board()
        sleep(0.25)
        board.print_board(board.backup_board)
        sleep(0.25)

    board.backup_board = []
