
from arithmetiqueDansZ import *

l = []
for k in range(2**16+1, 2**24, 2):
    if isprime(k):
        l.append(k)
        if len(l) % 10000 == 0:
            f = open("tp_primes.py", "w")
            f.write(f"pLen = {len(l)}\n")
            f.write(f"p = {l}")
            f.close()



