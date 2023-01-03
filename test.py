#with open("proxy_names.txt") as file:
#
#    file = file.readlines()
#
#    for line in file:
#        name = line.split('.')[1].strip()
#
#        print(name)

import csv
from random import choice


proxy = []
with open("names.csv") as file:

    file = csv.reader(file)

    for line in file:
        proxy.append(line[0])

with open("names.txt", 'w') as file:

    for name in proxy:

        file.writelines(name+',')

