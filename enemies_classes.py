from living_classes import Enemy


class Veloster(Enemy):

    def __init__(self):
        super().__init__()

        self.moves = 3
        self.moves_per_turn = 3

        self.cards["Hit"] = {"func": self.hit,
                             "level": "weak"}

        self.cards["Quicker"] = {"func": self.quicker,
                                 "level": "medium"}

        self.cards["Twist"] = {"func": self.twist,
                               "level": "strong"}

        self.init_cards()

    def hit(self):
        pass

    def twist(self):
        pass

    def quicker(self):
        self.moves = 4
