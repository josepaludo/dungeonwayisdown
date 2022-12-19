from random import randint
from time import sleep

from spec_classes import Warrior, Druid, Thief, Wizard, Priest
from living_classes import Enemy
from board_class import Board


def create_enemies(clas, board):

    num_min = randint(3, 6)
    num_max = num_min+(randint(1, 5))

    proxy = []

    for i in range(randint(num_min, num_max)):

        geni = clas(board)
        proxy.append(geni)

    return proxy


def create_players(board):

    proxy_list = []
    # for class_ in [Warrior, Druid, Thief, Wizard, Priest]:
    for class_ in [Warrior]:

        proxy = class_()
        if proxy.sym not in board.dead_players:
            proxy_list.append(proxy)

    for prox in proxy_list:
        prox.companions = proxy_list

    return proxy_list


def game_loop():

    board = Board()

    while True:

        players = create_players(board)
        enemies = create_enemies(Enemy, board)
        livings = enemies + players
        board.place_things(enemies, players)

        go_on = dungeon_loop(livings, board, players, enemies)

        if not go_on:
            break

        check_dead_players(board, players)


def dungeon_loop(livings, board, players, enemies):

    while True:

        dungeon_loop_check(livings, board, players, enemies)

        if all_players_died(players):
            return

        go_on = livings_turn(livings, board, players, enemies)

        if not go_on:
            return True


def livings_turn(livings, board, players, enemies):

    for living in livings:

        board.print_board()

        if board.level_finished(players, enemies):
            sleep(2)
            return

        if not living.dead:

            living_turn_check(board, living)

            if isinstance(living, Enemy):
                enemy_turn(living, board, players)

            else:
                player_turn(living, board, players, enemies)

    return True


def enemy_turn(enemy, board, players):

    board.make_copy()
    enemy.turn_move(players)
    enemy.blink_screen()
    board.empty_copy()


def blink_screen(board):
    """you must deal with proxy yourself!!!"""

    for i in range(2):
        sleep(0.05)
        board.print_board(board.backup_board)
        sleep(0.05)
        board.print_board()


def player_turn(player, board, players, enemies):

    player.maintance(board, enemies, players)

    input(f"{player.sym}'s turn. Press 'Enter' to begin.")

    while True:

        if player.dead:
            return

        valid_input = prompt_input(player, board)

        if not valid_input:
            return

        player.inputs[valid_input][0]()

        if valid_input not in ["move", "act"]:
            input("\nPress 'Enter' to return.")


def prompt_input(player, board):

    while True:

        board.print_board()
        print(f"{player.sym}'s turn.\n\nActions left: {player.actions}.\nMoves left: {player.moves}.\n")

        action = input("What do you want to do? ")

        if action == "end":
            return

        if action in player.inputs:
            return action

        print("\nInvalid input, enter 'help' for input options")
        input("\nPress 'Enter' to return.")


def living_turn_check(board, living):

    for func in board.living_turn_checker:

        remove_ = func(living)
        if remove_:
            board.living_turn_checker.remove(func)


def dungeon_loop_check(livings, board, players, enemies):
    pass


def all_players_died(players):

    for player in players:
        if not player.dead:
            return False

    return True


def check_dead_players(board, players):

    for player in players:
        if player.dead:

            board.dead_players.append(player.sym)

