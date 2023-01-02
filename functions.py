import os
from random import randint, choice
from time import sleep

from spec_classes import Warrior, Priest, Rogue
from druid_class import Druid
from wizard_class import Wizard
from enemies_classes import Goblin, Snake, Troll, Necro
from living_classes import Enemy
from board_class import Board
from miscellaneous import game_icon


def dungeon_way_is_down():

    start_game()

    result = game_loop()

    end_game(result)


def start_game():

    os.system('cls' if os.name == 'nt' else 'clear')

    print(game_icon)

    message ="A party of 5 adventurers enter a dungeon:\na warrior, a priest, "\
             "a druid, a wizard and a rogue.\n\nThe entry is shut.\n\n"\
             "The dungeon only way is down."

    print(message)

    input("\n\nPress 'Enter' to begin.")


def game_loop():

    board = Board()

    while True:

        game_finished = board_maintance(board)

        if game_finished:
            return True

        go_on = dungeon_loop(board)

        if not go_on:
            return

        board_clean_up(board)


def board_maintance(board):

    if board.game_finished():
        return True

    players = create_players(board)
    enemies = create_enemies(board)

    livings = enemies + players

    board.livings_maintance(livings, enemies, players, players)
    board.place_things()

    board.erase_log()
    board.erase_turn_checker()


def create_players(board):

    players = []

    for player_class in [Warrior, Priest, Druid, Wizard, Rogue]:

        player = player_class()

        if player.sym not in board.dead_players:
            player.board = board
            players.append(player)

    return players


def create_enemies(board):

    enemy_objects = []

    enemies = Goblin, Snake, Troll, Necro

    for i in range(board.level + 5):
        enemy_objects.append(create_enemy(board, enemies,
                                          True if i <= board.level else False))

    return enemy_objects


def create_enemy(board, enemy_classes, is_boss = False):

    enemy = choice(enemy_classes)()

    if is_boss:
        enemy.boss_maintance()

    enemy.board = board

    return enemy


def dungeon_loop(board):

    while True:

        if all_players_died(board):
            return

        board.log_maintance()

        go_on = livings_turns(board)

        if not go_on:
            return True


def all_players_died(board):

    for player in board.players:
        if not player.dead:
            return False

    return True


def livings_turns(board):

    for living in board.livings:

        board.print_board()

        if board.level_finished():
            board.level_finished_warning()
            return

        if living.dead:
            dead_living_maintance(living)
            continue

        living_turn_check(living)

        do_turn(living)

    return True


def dead_living_maintance(living):

    living.revive_counter -= 1


def living_turn_check(living):

    for func in living.board.living_turn_checker:

        remove_ = func(living)
        if remove_:
            living.board.living_turn_checker.remove(func)


def do_turn(living):

    if living in living.board.enemies:
        living_turn(living, True)

    elif living in living.board.players:
        player_turn(living)

    else:
        living_turn(living, False)


def living_turn(living, is_enemy):

    living.living_maintance()

    if living.can_move:
        living_move(living, is_enemy)

    living_act(living)
    living.empty_hand()


def living_move(living, is_enemy):

    for i in range(living.moves):

        if living.check_if_dead():
            break

        living.board.make_copy()
        living.turn_move(is_enemy)
        living.board.board_blink()
        living.board.empty_copy()

    if living.moves_changed_counter > 0:
        living.moves_changed_counter -= 1

    else:
        living.moves = living.moves_per_turn


def living_act(living):

    for card in living.my_cards:

        living.board.make_copy()
        living.cards[card]["func"]()
        living.board.board_blink()
        living.board.empty_copy()

    if living.actions_changed_counter > 0:
        living.actions_changed_counter -= 1

    else:
        living.actions = living.actions_per_turn


def player_turn(player):

    player.player_maintance()

    input(f"{player.sym}'s turn. Press 'Enter' to begin.")

    while True:

        if player.dead:
            return

        valid_input = prompt_input(player)

        if not valid_input:
            return

        player.inputs[valid_input]["func"]()

        if valid_input not in ["move", "act"]:
            input("\nPress 'Enter' to return.")


def prompt_input(player):

    while True:

        player.board.print_board()
        print(f"{player.sym}'s turn.\n\nActions left: {player.actions}.\n"\
              f"Moves left: {player.moves}.\n")

        action = input("What do you want to do? ('help' for options)\n")

        if action == "end":
            return

        if action in player.inputs:
            return action

        player.wrong_input_warning()


def board_clean_up(board):

    board.clear_livings()
    board.check_dead_players()


def end_game(result):

    os.system('cls' if os.name == 'nt' else 'clear')

    print(game_icon)

    win_message = "The way is shut.\n\n"\
                  "The light is out.\n\n"\
                  "The dungeon is over."
    loss_message = "Your party was not able to follow the dungeon way."

    print(win_message if result else loss_message)

    input("\n\nPress 'Enter' to exit.")

    os.system('cls' if os.name == 'nt' else 'clear')

