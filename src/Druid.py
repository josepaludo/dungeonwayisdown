from Player import Player, Ally


class Beast(Ally):

    def __init__(self):
        super().__init__()

        self.bite_damage = 0
        self.claw_damage = 0
        self.bite_name = "bite"
        self.rip_name = "claw"
        self.attack_range = 1

    def bite(self):

        self.urdl_damage(self.claw_sym, self.bite_damage, \
                         self.bite_name, False, False)

    def rip(self):

        self.around_damage(self.claw_sym, self.claw_damage, \
                           self.rip_name, False, self.attack_range)

    def rip_and_bite(self):

        self.bite()
        self.rip()

    def wild_sprint(self):

        self.moves = max(self.moves+1, self.moves_per_turn+1)
        self.moves_changed_counter += 1

    def wild_action(self):

        self.actions = max(self.actions+1, self.actions_per_turn+1)
        self.actions_changed_counter += 1

    def wild_calling(self):

        self.wild_sprint()
        self.wild_action()

        message = f"{self.name} echoes a wild call, "\
                   "getting faster and more active."
        self.board.add_log(message)


class Wolf(Beast):

    def __init__(self):
        super().__init__()

        self.sym = 'u'
        self.name = "Wolf"

        self.health = 15

        self.claw_damage = 2
        self.bite_damage = 3

        self.cards["Bite"] = {"func": self.bite,
                              "level": "weak"}

        self.cards["Rip"] = {"func": self.rip,
                             "level": "medium"}

        self.cards["Rip and Bite"] = {"func": self.rip_and_bite,
                                      "level": "strong"}

        self.init_cards()


class Boar(Beast):

    def __init__(self):
        super().__init__()

        self.sym = 'a'
        self.name = "Boar"
        self.rip_name = "tusk"

        self.health = 10

        self.moves_per_turn = 2
        self.moves = self.moves_per_turn

        self.claw_damage = 3

        self.cards['Tusk Strike'] = {"func": self.rip,
                                     "level": "weak"}

        self.cards['Boar Sprint'] = {"func": self.boar_sprint,
                                     "level": "medium"}

        self.cards['Boar Enrage'] = {"func": self.boar_enrage,
                                     "level": "strong"}

        self.init_cards()

    def boar_sprint(self):

        self.wild_sprint()

        message = f"{self.name} echoes a wild call, getting faster."
        self.board.add_log(message)

    def boar_enrage(self):

        self.wild_action()

        message = f"{self.name} echoes a wild call, geting more active."
        self.board.add_log(message)


class Bear(Beast):

    def __init__(self):
        super().__init__()

        self.sym = "b"
        self.name = "Bear"

        self.health = 20

        self.claw_damage = 3
        self.bite_damage = 4

        self.short_taunt_duration = 2

        self.barkskin_health = 5

        self.cards["Rip and Bite"] = {"func": self.rip_and_bite,
                                      "level": "weak"}

        self.cards["Barkskin"] = {"func": self.barkskin,
                                  "level": "medium"}

        self.cards["Short Taunt"] = {"func": self.do_short_taunt,
                                      "level": "strong"}

        self.init_cards()


class Tiger(Beast):

    def __init__(self):
        super().__init__()

        self.sym = "t"
        self.name = "Tiger"

        self.claw_damage = 3
        self.bite_damage = 4

        self.frenzy_range_increase = 1
        self.frenzy_damage_increase = 1

        self.cards["Rip and Bite"] = {"func": self.rip_and_bite,
                                      "level": "weak"}

        self.cards["Best Frenzy"] = {"func": self.beast_frenzy,
                                     "level": "medium"}

        self.cards["Wild Calling"] = {"func": self.wild_calling,
                                      "level": "strong"}

        self.init_cards()

    def beast_frenzy(self):

        self.attack_range += self.frenzy_range_increase
        self.claw_damage += self.frenzy_damage_increase

        self.rip()

        self.attack_range -= self.frenzy_range_increase
        self.claw_damage -= self.frenzy_damage_increase


class Druid(Player):

    def __init__(self):
        super().__init__()

        self.sym = "D"
        self.name = "Druid"

        self.root_sym = "z"
        self.saber_tooth_tiger_sym = "T"
        self.mammoth_sym = "M"
        self.druid_sym = "D"

        self.mm_damage_sym = "p"
        self.stt_damage_sym = "p"

        self.enroot_turns = 1
        self.enrooted = []

        self.mammoth_health = 35
        self.saber_tooth_tiger_health = 25
        self.druid_health = 20

        self.mammoth_moves_per_turn = 1
        self.saber_tooth_tiger_moves_per_turn = 2
        self.druid_moves_per_turn = 1

        self.stt_bite_damage = 3
        self.stt_bite_reach = 2
        self.stt_bite_amount = 3
        self.stt_rip_damage = 4
        self.stt_rip_reach = 2
        self.stt_wild_call_amount = 2

        self.mm_tusk_damage = 5
        self.mm_trunk_damage = 4
        self.mm_trunk_reach = 2
        self.mm_tusk_reach = 2

        self.short_taunt_duration = 2
        self.barkskin_health = 10

        self.mammoth_name = "Mammoth"
        self.saber_tooth_tiger_name = "Saber Tooth Tiger"
        self.druid_name = "Druid"

        self.reverse_transformation_card = "Reverse Transformation"
        self.reverse_info = {"func": self.reverse_transformation,
                             "descr": "Transforms back into your regular form.",
                             "level": None}

        self.entangle_descr = f"Protects an ally, enrooting enemies around it "\
                              f"for {self.enroot_turns} turn"\
                              f"{'.' if self.enroot_turns == 1 else 's.'}"

        self.enroot_descr = f"Enroots all enemies for {self.enroot_turns} turn"\
                            f"{'.' if self.enroot_turns == 1 else 's.'}"

        self.summon_wild_descr = "Summons an wild beast: a boar or a wolf."
        self.summon_beast_descr = "Summons an wild beast: a bear of a tiger."
        self.ancient_shape_descr = "Transforms into an ancient beast, "\
                                   "a saber tooth tiger or a mammoth."

        self.stt_bite_descr = f"Bites an enemy, dealing {self.stt_bite_damage}"
        self.stt_rip_descr = f"Rips all enemies around you, "\
                             f"dealing {self.stt_rip_damage}"
        self.stt_wild_call_descr = f"Echoes a wild call, gaining "\
                                   f"{self.stt_wild_call_amount} more "\
                                   f"movements, actions and cards"

        self.mm_trunk_swipe_descr = f"Swipes your trunk, deaking "\
                                    f"{self.mm_trunk_damage} damage."
        self.mm_tusk_bash_descr = f"Bash enemies in front of you, dealing "\
                                  f"{self.mm_tusk_damage} damage."
        self.mm_ancient_taunt_descr = "Taunts enemies and toughens your skin."

        self.get_druid_cards()

    def get_druid_cards(self):

        self.cards, self.my_cards = {}, []

        self.get_player_cards()
        self.init_druid_cards()
        self.init_cards()

    def init_druid_cards(self):

        self.cards["Entangle"] = {"func": self.entangle,
                                  "descr": self.entangle_descr,
                                  "level": "weak"}

        self.cards["Enroot"] = {"func": self.enroot,
                                  "descr": self.enroot_descr,
                                  "level": "medium"}

        self.cards["Summon Wild"] = {"func": self.summon_wild,
                                  "descr": self.summon_wild_descr,
                                  "level": "medium"}

        self.cards["Summon Beast"] = {"func": self.summon_beast,
                                  "descr": self.summon_beast_descr,
                                  "level": "strong"}

        self.cards["Ancient Shape"] = {"func": self.ancient_shape,
                                  "descr": self.ancient_shape_descr,
                                  "level": "strong"}


    def entangle(self):

        question = "Which ally would you like to protect with your roots?"
        ally = self.prompt_for_ally(question)

        if not ally:
            return

        self.do_entangle(ally)

        self.append_to_turn_checker(self.disenroot)

        return True

    def do_entangle(self, ally):

        around_coords = self.get_around_coords(ally.y, ally.x, 1)

        for coord in around_coords:

            target = self.check_coord(coord[0], coord[1])

            if target == 'invalid':
                continue

            self.board.backup_board[coord[0]][coord[1]] = self.root_sym

            if target not in self.board.enemies:
                continue

            message = f"{target.name} is entangled on {self.name}'s roots."
            self.board.add_log(message)

            self.enrooted.append(target)
            target.can_move = False

    def disenroot(self, living):

        if self != living:
            return

        for enemy in self.enrooted:
            enemy.can_move = True

        self.enrooted = []

        message = f"Enrooted enemies freed themselves from {self.name}'s roots"
        self.board.add_log(message)

        return True

    def enroot(self):

        question = "Do you want to enroot all enemies? "\
                   "Enter '1' for yes or 'q' for no."
        go_on = self.yes_no_input(question)

        if not go_on:
            return

        self.do_enroot()

        self.append_to_turn_checker(self.disenroot)

        message = f"All enemyes are entangled on {self.name}'s roots."
        self.board.add_log(message)

        return True

    def do_enroot(self):

        for enemy in self.board.enemies:

            if enemy.dead:
                continue

            self.board.backup_board[enemy.y][enemy.x] = self.root_sym

            enemy.can_move = False
            self.enrooted.append(enemy)

    def summon_wild(self, class_1=Boar, class_2=Wolf,
                    name_1="Boar", name_2="Wolf"):

        summon = self.prompt_for_wild(name_1, name_2)

        if not summon:
            return

        wild_class = (class_1, class_2)[summon-1]

        self.summon_enemy_ally(wild_class, is_enemy=False)

        return True

    def prompt_for_wild(self, wild_1, wild_2, presentation=None, question=None):

        presentation = presentation if presentation \
                       else "Wild beasts you can summon"
        question = question if question \
                   else "Which one would you like to summon"

        while True:

            self.clear_screen()

            print(f"{presentation}:\n\n'1' for {wild_1}.\n"\
                  f"'2' for {wild_2}.\n'q' to quit.")
            answer = input(f"\n{question}?")

            if answer == 'q':
                return

            if self.check_int_range(answer, 1, 2):
                return int(answer)

            self.wrong_input_warning()

    def summon_beast(self):

        if self.summon_wild(Bear, Tiger, "Bear", "Tiger"):
            return True

    def ancient_shape(self):

        presentation = "Ancient beasts"
        question = "Wich one would you like to transform into"
        ancient_beasts = "Saber Tooth Tiger", "Mammoth"

        answer = self.prompt_for_wild(ancient_beasts[0], ancient_beasts[1],
                                      presentation, question)

        if not answer:
            return

        if answer == 1:
            info = self.get_saber_tooth_tiger_info()
        else:
            info = self.get_mammoth_info()

        self.transform(info)

    def transform(self, info):

        sym, health, moves_per_turn, name, get_cards = info

        self.sym = sym
        self.health = health
        self.moves_per_turn = moves_per_turn
        self.name = name
        get_cards()

        self.board.board[self.y][self.x] = self.sym

        self.actions -= 1
        self.board.board_blink()

    def get_druid_info(self):

        return self.druid_sym, self.druid_health, self.druid_moves_per_turn, \
               self.druid_name, self.get_druid_cards

    def get_mammoth_info(self):

        return self.mammoth_sym, self.mammoth_health, \
               self.mammoth_moves_per_turn, self.mammoth_name, \
               self.get_mammoth_cards

    def get_saber_tooth_tiger_info(self):

        return self.saber_tooth_tiger_sym, self.saber_tooth_tiger_health, \
               self.saber_tooth_tiger_moves_per_turn, \
               self.saber_tooth_tiger_name, self.get_saber_tooth_tiger_cards

    def get_saber_tooth_tiger_cards(self):

        self.cards, self.my_cards = {}, []

        self.cards["Bite"] = {"func": self.stt_bite,
                              "descr": self.stt_bite_descr,
                              "level": "weak"}

        self.cards["Rip"] = {"func": self.stt_rip,
                             "descr": self.stt_rip_descr,
                             "level": "medium"}

        self.cards["Wild Call"] = {"func": self.stt_wild_call,
                                   "descr": self.stt_wild_call_descr,
                                   "level": "strong"}

        self.init_cards()

        self.get_reverse_transformation_card()

        for i in range(2):
            self.get_turn_cards()

    def get_mammoth_cards(self):

        self.cards, self.my_cards = {}, []

        self.cards["Tusk Bash"] = {"func": self.mm_tusk_bash,
                                   "descr": self.mm_tusk_bash_descr,
                                   "level": "weak"}

        self.cards["Trunk Swipe"] = {"func": self.mm_trunk_swipe,
                                     "descr": self.mm_trunk_swipe_descr,
                                     "level": "medium"}

        self.cards["Ancient Taunt"] = {"func": self.mm_ancient_taunt,
                                       "descr": self.mm_ancient_taunt_descr,
                                       "level": "strong"}

        self.init_cards()

        self.get_reverse_transformation_card()

        for i in range(2):
            self.get_turn_cards()

    def get_reverse_transformation_card(self):

        self.cards[self.reverse_transformation_card] = self.reverse_info
        self.my_cards.append(self.reverse_transformation_card)

    def reverse_transformation(self):

        info = self.get_druid_info()
        self.transform(info)

    def stt_bite(self):

        question = f"Do you wish to bite your enemies "\
                   f"{self.stt_bite_amount} times?"

        go_on = self.yes_no_input(question)

        if not go_on:
            return

        message = f"{self.name} dealt {self.stt_bite_damage} damage "\
                  f"to # with its bite."

        for i in range(self.stt_bite_amount):
            self.players_urdl_damage(self.stt_bite_reach, self.stt_damage_sym,
                                     self.stt_bite_damage, message)

        return True

    def stt_rip(self):

        message = f"{self.name} dealt {self.stt_rip_damage} damage"\
                  f"to # with its claws."
        question = "Do you wish to rip your enemies with your claws?"

        if self.player_around_damage(self.stt_rip_reach, self.stt_damage_sym,
                                     self.stt_rip_damage, message, question):
            return True

    def stt_wild_call(self):

        question = "Do you wish to echo a will call, "\
                   "getting faster and more active?"

        go_on = self.yes_no_input(question)

        if not go_on:
            return

        for i in range(self.stt_wild_call_amount):
            self.moves += 1
            self.actions += 1
            self.get_turn_cards()

        x = self.stt_wild_call_amount
        message = f"{self.name} echoes a wild call, gaining {x} moves, "\
                  f"{x} actions and {x} cards."
        self.board.add_log(message)

    def mm_tusk_bash(self):

        message = f"{self.name} dealt {self.mm_tusk_damage} damage "\
                  f"to # with its tusks."

        if self.players_urdl_damage(self.tusk_reach, self.mm_damage_sym,
                                    self.mm_tusk_damage, message):
            return True

    def mm_trunk_swipe(self):

        message = f"{self.name} dealt {self.mm_trunk_damage} damage"\
                  f"to # with its trunk."
        question = "Do you wish to perform the mammoth's swipe?"

        if self.player_around_damage(self.mm_trunk_reach, self.mm_damage_sym,
                                     self.mm_trunk_damage, message, question):
            return True

    def mm_ancient_taunt(self):

        question = "Are you sure you want to taunt enemies and "\
                   "become more resilient? '1' for yes, 'q' for no."
        go_on = self.yes_no_input(question)

        if not go_on:
            return

        self.do_short_taunt()
        self.barkskin()

        return True

