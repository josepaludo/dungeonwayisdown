from living_classes import Enemy
from player_class import Player, Ally


class Veloster(Enemy):

    def __init__(self):
        super().__init__()

        self.sym = 'v'
        self.name = "Veloster"

        self.moves = 3
        self.moves_per_turn = 3

        self.knife_sym = "k"
        self.knife_damage = 3

        self.cards["Hit"] = {"func": self.hit,
                             "level": "weak"}

        self.cards["Quicker"] = {"func": self.quicker,
                                 "level": "medium"}

        self.cards["Twist"] = {"func": self.twist,
                               "level": "strong"}

        self.init_cards()

    def hit(self):

        if not self.can_attack:
            return

        coords = self.get_urdl_coords(self.y, self.x, 1)
        for coord in coords:

            ycor, xcor = coord[0][0], coord[0][1]

            target = self.check_coord(ycor, xcor)
            if target in self.board.allies:

                self.make_hit(target, ycor, xcor)

                return

    def make_hit(self, target, ycor, xcor):

        self.board.backup_board[ycor][xcor] = self.knife_sym

        if target.invulnerable or target.dead:
            return

        self.target.health -= self.knife_damage

        message = f"{self.name} dealt {self.knife_damage} to {target.name} with his knife."
        self.board.add_log(message)

    def twist(self):

        if not self.can_attack:
            return

        coords = self.get_around_coords(self.y, self.x, 1)

        for coord in coords:

            target = self.check_coord(coord[0], coord[1])

            self.make_twist(coord[0], coord[1], target)

    def make_twist(self, ycor, xcor, target):

        if target == 'invalid':
            return

        self.board.backup_board[ycor][xcor] = self.knife_sym

        if target in self.board.allies:

            if target.invulnerable or target.dead:
                return

            target.health -= self.knife_damage

            message = f"{self.name} made a twist and dealt {self.knife_damage} to {target.name} with his knife."
            self.board.add_log(message)

    def quicker(self):

        self.moves = 4
