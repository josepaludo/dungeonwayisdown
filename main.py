from random import randint

from classes import Thing, Living, Enemy, Board
from functions import create_enemies, game_icon


board = Board()

things = []

exit = randint(1, 4)
entry = 1 if exit==3 else 2 if exit==4 else 3 if exit==1 else 4
num_min = randint(1, 5)
num_max = num_min+(randint(1, 5))

enemies = create_enemies(Enemy, entry, board, num_min, num_max)
things += enemies

board.place_things(things)

board.print_board()
