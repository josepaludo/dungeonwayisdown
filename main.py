from random import randint
from time import sleep

from board_class import Board
from living_classes import Thing, Living, Enemy
from functions import create_enemies, create_players, prepare_turn, get_entry, game_icon


board = Board()

while True:

    sleep(5)
    enemies, player = prepare_turn(board)
