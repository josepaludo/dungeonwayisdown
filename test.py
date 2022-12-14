a = [x for x in range(1, 11)]

for i in range(4):
    if i%2==0:
        print(a[i if i==2 else -1])
