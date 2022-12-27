class A:

    def __init__(self):

        self.name = "Idiot"
    def del_self(self):
        del self

a = A()

a.del_self()

print(a.name)


