from random import randint, choice
from time import sleep

from spec_classes import Warrior, Druid, Thief, Wizard, Priest
from living_classes import Enemy
from board_class import Board


def create_enemies(clas, board):

    num_min = randint(3, 6)
    num_max = num_min+(randint(1, 5))

    proxy = []

    for i in range(randint(num_min, num_max)):

        geni = clas()
        geni.board = board
        proxy.append(geni)

    return proxy


def create_players(board):

    proxy_list = []
    # for class_ in [Warrior, Druid, Thief, Wizard, Priest]:
    for class_ in [Warrior]:

        proxy = class_()
        if proxy.sym not in board.dead_players:
            proxy.board = board
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
        allies = players

        board.livings_maintance(livings, enemies, allies, players)
        board.place_things()

        go_on = dungeon_loop(board)

        if not go_on:
            break

        check_dead_players(board, players)

        board.clear_livings()


def dungeon_loop(board):

    while True:

        dungeon_loop_check(board)

        if all_players_died(board):
            return

        go_on = livings_turn(board)

        if not go_on:
            return True


def livings_turn(board):

    for living in board.livings:

        board.print_board()

        if board.level_finished():
            sleep(2)
            return

        if not living.dead:

            living_turn_check(board, living)

            if isinstance(living, Enemy):
                enemy_turn(living, board)

            else:
                player_turn(living, board)

    return True


def enemy_turn(enemy, board):

    enemy.enemy_maintance()

    enemy_move(enemy, board)

    enemy_act(enemy, board)

    enemy.empty_hand()


def enemy_act(enemy, board):
    pass

    #for i in range(enemy.actions):
     #   card = choice(enemy.card_list)
      #  board.make_copy()
       # enemy.cards[card]["func"]()
       # board.board_blink()
        #board.empty_copy()

    #enemy.actions = 0


def enemy_move(enemy, board):

    for i in range(enemy.moves):

        board.make_copy()
        enemy.turn_move()
        board.board_blink()
        board.empty_copy()

    enemy.moves = 0


def player_turn(player, board):

    player.player_maintance()

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


def dungeon_loop_check(board):
    pass


def all_players_died(board):

    for player in board.players:
        if not player.dead:
            return False

    return True


def check_dead_players(board):

    for player in board.players:
        if player.dead:

            board.dead_players.append(player.sym)

