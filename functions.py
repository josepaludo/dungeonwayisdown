from random import randint

def get_entry(exit):
    return 1 if exit==3 else 2 if exit==4 else 3 if exit==1 else 4


def create_enemies(Clas, entry, board, n_min, n_max):
    """entry must be 1, 2, 3, 4 standing for up, right, down, left"""

    proxy = []

    for i in range(randint(n_min, n_max)):

        for i in range(50):

            xrange = (0, 19) if entry%2!=0 else (0, 9) if entry==2 else (10, 19)
            yrange = (0, 19) if entry%2==0 else (0, 9) if entry==3 else (10, 19)
            xpos = randint(xrange[0], xrange[1])
            ypos = randint(yrange[0], yrange[1])
            print(xpos, ypos)
            print(board.board)

            if board.board[ypos][xpos] == board.empty_square:

                geni = Clas()
                geni.x, geni.y, geni.sym = xpos, ypos, "e"
                proxy.append(geni)

                break

    return proxy


game_icon = """
______
|  _  |
| | | |_   _ _ __   __ _  ___  ___  _ __
| | | | | | | '_ \ / _` |/ _ \/ _ \| '_  |
| |/ /| |_| | | | | (_| |  __/ (_) | | | |
|___/  \__,_|_| |_|\__, |\___|\___/|_| |_|
                    __/ |
                   |___/
    _    _
   | |  | |
   | |  | | __ _ _   _
   | |/\| |/ _` | | | |
   \  /\  / (_| | |_| |
    \/  \/ \__,_|\__, |
                  __/ |
                 |___/
  _      ______
 (_)     |  _  |
  _ ___  | | | |_____      ___ __
 | / __| | | | / _ \ \ /\ / / '_  |
 | \__ \ | |/ / (_) \ V  V /| | | |
 |_|___/ |___/ \___/ \_/\_/ |_| |_|
\n"""
