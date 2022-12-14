from random import randint

from board_class import Board
from living_classes import Thing, Living, Enemy
from functions import create_enemies,get_entry, game_icon


board = Board()

livings = []

num_min = randint(3, 6)
num_max = num_min+(randint(1, 5))

enemies = create_enemies(Enemy, num_min, num_max)
livings += enemies
board.place_things(livings)


board.print_board()
