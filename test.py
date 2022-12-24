a = ["a", "b", "c"]

b = ""

for ind, x in enumerate(a):
    b += f"{x}{'.' if ind == len(a)-1 else ', '}"

print(b)
