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

        coords = self.get_urdl_coords(self.y, self.x, 1)[0]
        for coord in coords:
            info = self.check_coords(coord[0], coord[1])
            if info[0]:
                self.make_hit(info, coord[0], coord[1])
                return

    def make_hit(self, target, ycor, xcor):



    def twist(self):
        pass

    def quicker(self):
        self.moves = 4
