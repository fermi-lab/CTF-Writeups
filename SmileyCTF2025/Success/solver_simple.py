from itertools import product
from string import printable

for x, y in product(printable, repeat=2):
    if ord(y) * ord(x) == 3366:
        print(f"chars[37]={repr(x)}, chars[15]={repr(y)}")
