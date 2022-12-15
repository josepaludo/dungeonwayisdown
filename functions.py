from random import randint
from copy import deepcopy
from time import sleep

from player_class import Warrior, Druid, Thief, Wizard, Priest
from living_classes import Enemy


def get_entry(exit):
    return 1 if exit==3 else 2 if exit==4 else 3 if exit==1 else 4


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
