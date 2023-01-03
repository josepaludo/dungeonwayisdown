from random import choice, randint


with open("names.txt") as file:

    file = file.readlines()[0].split(',')
    file.pop(-1)


    print(file.pop(randint(0, len(file)-1)))
