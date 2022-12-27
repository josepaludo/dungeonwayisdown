from player_class import Player, Ally

class Beast(Ally):

    def __init__(self):
        super().__init__()

        self.bite_damage = 0
        self.claw_damage = 0
        self.bite_name = "bite"
        self.rip_name = "claw"
        self.attack_range = 1

    def bite(self):

        self.urdl_damage(self.claw_sym, self.bite_damage, self.bite_name, False, False)

    def rip(self):

        self.around_damage(self.claw_sym, self.claw_damage, self.rip_name, False, self.attack_range)

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

        message = f"{self.name} echoes a wild call, getting faster and more active."
        self.board.add_log(message)

    def barkskin(self):

        self.health += 5

        message = f"{self.name} toughens its skin, becoming more resilient."
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

        self.cards["Rip and Bite"] = {"func": self.rip_and_bite,
                                      "level": "weak"}

        self.cards["Barkskin"] = {"func": self.barkskin,
                                  "level": "medium"}

        self.cards["Short Taunt"] = {"func": self.short_taunt,
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

        self.boar_sym = "r"
        self.wolf_sym = "w"
        self.tiger_sym = "t"
        self.bear_sym = "b"

        self.saber_tooth_tiger_sym = "T"
        self.mammoth_sym = "M"

        self.enroot_turns = 1

        self.enrooted = []

        entangle = f"Protects an ally, enrooting enemies around it for {self.enroot_turns} turn{'.' if self.enroot_turns == 1 else 's.'}"
        enroot = f"Enroots all enemies for {self.enroot_turns} turn{'.' if self.enroot_turns == 1 else 's.'}"
        summon_wild = "Summons an wild beast: a boar or a wolf."
        summon_beast = "Summons an wild beast: a bear of a tiger."
        ancient_shape = "Transforms into an ancient beast, a saber tooth tiger or a mammoth."

        self.cards["Entangle"] = {"func": self.entangle,
                                  "descr": entangle,
                                  "level": "weak"}

        self.cards["Enroot"] = {"func": self.enroot,
                                  "descr": enroot,
                                  "level": "medium"}

        self.cards["Summon Wild"] = {"func": self.summon_wild,
                                  "descr": summon_wild,
                                  "level": "medium"}

        self.cards["Summon Beast"] = {"func": self.summon_beast,
                                  "descr": summon_beast,
                                  "level": "strong"}

        self.cards["Ancient Shape"] = {"func": self.ancient_shape,
                                  "descr": ancient_shape,
                                  "level": "strong"}

        self.init_cards()

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

        question = "Do you want to enroot all enemies? Enter '1' for yes or 'q' for no."
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

    def summon_wild(self, class_1=Boar, class_2=Wolf, name_1="Boar", name_2="Wolf"):

        summon = self.prompt_for_wild(name_1, name_2)

        if not summon:
            return

        wild_class = (class_1, class_2)[summon-1]

        self.summon_enemy_ally(wild_class, is_enemy=False)

        return True

    def prompt_for_wild(self, wild_1, wild_2):

        while True:

            self.clear_screen()

            print(f"Wild beasts you can summon:\n\n'1' for {wild_1}.\n'2' for {wild_2}.\n'q' to quit.")
            answer = input("\nWhich one would you like to summon?")

            if answer == 'q':
                return

            if self.check_int_range(answer, 1, 2):
                return int(answer)

            self.wrong_input_warning()

    def summon_beast(self):

        self.summon_wild(Bear, Tiger, "Bear", "Tiger")

    def ancient_shape(self):
        pass
