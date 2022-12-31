from random import randint


class A:

    def __init__(self):

        self.a = []

class B:

    def __init__(self):

        self.name = "b name"

a = A()

for i in range(10):

    generic = B()

    a.a.append(generic)

l = [f for f in a.a]

def print_l_aa():
    for i in range(len(a.a)):
        print(a.a[i])
        try:
            print(l[i])
        except IndexError:
            print("error")
    print(i)

print_l_aa()

for i in range(5):

    p = l.pop(randint(0, len(l)-1))

print_l_aa()
