from itertools import product

a = []
s = 0
for i in product('КОМПАНИЯ', repeat=6):
    a += [''.join(i)]
a.sort()
for i in range(len(a)):
    if i % 2 != 0 and a[i][0] != 'М' and a[i].count('И') == 3:
        s += 1
print(s)
