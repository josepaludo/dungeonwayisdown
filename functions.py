from random import randint

def get_entry(exit):
    return 1 if exit==3 else 2 if exit==4 else 3 if exit==1 else 4


def create_enemies(Clas, n_min, n_max):

    proxy = []

    for i in range(randint(n_min, n_max)):

        geni = Clas()
        proxy.append(geni)

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
