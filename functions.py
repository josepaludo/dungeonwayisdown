from random import randint, choice
from time import sleep

from spec_classes import Warrior, Thief, Wizard, Priest
from druid_class import Druid
from enemies_classes import Goblin, Snake, Troll, Necro
from living_classes import Enemy
from board_class import Board


def create_enemies(board):

    enemies = []

    for i in range(5+randint(0, 5)):

        enemy_classes = Snake, Goblin, Troll, Necro
        enemy = choice(enemy_classes)()

        enemy.board = board
        enemies.append(enemy)

    return enemies


def create_players(board):

    players = []
    for player_class in [Warrior, Priest, Druid]:

        player = player_class()

        if player.sym not in board.dead_players:
            player.board = board
            players.append(player)

    return players


def game_loop():

    board = Board()

    while True:

        players = create_players(board)
        enemies = create_enemies(board)

        livings = enemies + players

        board.livings_maintance(livings, enemies, players, players)
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

        if living.dead:
            continue

        living_turn_check(board, living)

        if living in board.enemies:
            living_turn(living, board)

        elif living in board.players:
            player_turn(living, board)

        else:
            living_turn(living, board)

    return True


def living_turn(living, board):

    living.living_maintance()
    living_move(living, board)
    living_act(living, board)
    living.empty_hand()


def living_act(living, board):

    for card in living.my_cards:

        board.make_copy()
        living.cards[card]["func"]()
        board.board_blink()
        board.empty_copy()

    if living.actions_changed_counter > 0:
        living.actions_changed_counter -= 1

    else:
        living.actions = living.actions_per_turn

def living_move(living, board):

    for i in range(living.moves):

        board.make_copy()
        living.turn_move()
        board.board_blink()
        board.empty_copy()

    if living.moves_changed_counter > 0:
        living.moves_changed_counter -= 1

    else:
        living.moves = living.moves_per_turn


def player_turn(player, board):

    player.player_maintance()

    input(f"{player.sym}'s turn. Press 'Enter' to begin.")

    while True:

        if player.dead:
            return

        valid_input = prompt_input(player, board)

        if not valid_input:
            return

        player.inputs[valid_input]["func"]()

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

        player.wrong_input_warning()


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

