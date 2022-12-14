from random import randint

from board_class import Board
from living_classes import Thing, Living, Enemy
from functions import create_enemies, create_players, get_entry, game_icon


board = Board()

livings = []


enemies = create_enemies(Enemy)
players = create_players()
livings += enemies
livings += players
board.place_things(enemies, Players)


board.print_board()
for player in players:
    print(player, player.sym)
