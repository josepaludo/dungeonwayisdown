from random import randint

from classes import Thing, Living, Enemy, Board
from functions import create_enemies,get_entry, game_icon


board = Board()

things = []

#exit = randint(1, 4)
#entry = get_entry(exit)
num_min = randint(1, 5)
num_max = num_min+(randint(1, 5))

enemies = create_enemies(Enemy, 3, board, num_min, num_max)
things += enemies

board.place_things(things)

board.print_board()
