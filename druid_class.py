from player_class import Player, Ally

class Tiger(Ally):

    def __init__(self):
        super().__init__()

        pass

class Boar(Ally):

    def __init__(self):
        super().__init__()

        self.sym = 'a'
        self.name = "Boar"

        self.health = 10

        self.moves = 2
        self.moves_per_turn = 2

        self.actions_per_turn = 1

        self.tusk_damage = 3

        self.cards['Tusk Strike'] = {"func": self.tusk_strike,
                                     "level": "weak"}

        self.cards['Boar Sprint'] = {"func": self.boar_sprint,
                                     "level": "medium"}

        self.cards['Boar Enrage'] = {"func": self.boar_enrage,
                                     "level": "strong"}

        self.init_cards()

    def tusk_strike(self):

        coords = self.get_around_coords(self.y, self.x, 1)

        for coord in coords:

            ycor, xcor = coord[0], coord[1]

            target = self.check_coord(ycor, xcor)

            self.do_tusk_strike(ycor, xcor, target)

    def do_tusk_strike(self, ycor, xcor, target):

        if target == 'invalid':
            return

        self.board.backup_board[ycor][xcor] = self.claw_sym

        if target in self.board.enemies:

            if target.dead:
                return

            target.health -= self.tusk_damage

            message = f"{self.name} hit {target.name} with its tusks, dealing {self.tusk_damage}."
            self.board.add_log(message)

            target.check_if_dead(self)

    def boar_sprint(self):

        self.moves = max(self.moves+1, self.moves_per_turn+1)
        self.moves_changed_counter += 1

    def boar_enrage(self):

        self.actions = max(self.actions+1, self.actions_per_turn+1)
        self.actions_changed_counter += 1

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

    def summon_wild(self):

        summon = self.prompt_for_wild()

        if not summon:
            return

        wild_class = (Boar, Tiger)[summon-1]

        self.summon_enemy_ally(wild_class, is_enemy=False)

        return True

    def prompt_for_wild(self):

        while True:

            self.clear_screen()

            print("Wild beasts you can summon:\n\n'1' for Boar.\n'2' for Tiger.\n'q' to quit.")
            answer = input("\nWhich one would you like to summon?")

            if answer == 'q':
                return

            if self.check_int_range(answer, 1, 2):
                return int(answer)

            self.wrong_input_warning()

    def summon_beast(self):
        pass

    def ancient_shape(self):
        pass
