from enemies_classes import Goblin, Snake, Troll, Necro


class GoblinBoss(Goblin):
    def __init__(self):
        super().__init__()

        self.sym = self.sym.title()
        self.name += " Boss"

        self.moves = 3
        self.moves_per_turn = 3

        self.actions_per_turn = 2

        self.knife_damage = 3

        self.twist_range = 1


class SnakeBoss(Snake):

    def __init__(self):
        super().__init__()

        self.sym = self.sym.title()
        self.name += " Boss"

        self.health = 15

        self.poison_damage = 2
        self.poison_dot_damage = 1
        self.dot_turn_duration = 3
        self.spit_range = 5
        self.spray_range = 2


class TrollBoss(Troll):

    def __init__(self):
        super().__init__()

        self.sym = self.sym.title()
        self.name += " Boss"

        self.health = 30

        self.rock_damage = 4
        self.boulder_damage = 5
        self.splah_damage = 3

        self.throw_rock_range = 10
        self.throw_boulder_range = 6
        self.splash_range = 2


class NecroBoss(Necro):

    def __init__(self):
        super().__init__()

        self.sym = self.sym.title()
        self.name += " Boss"

        self.health = 15

        self.moves = 0
        self.moves_per_turn = 0

        self.actions_per_turn = 1

        self.drain_life_damage = 1

