from math import sqrt, e
from random import random, shuffle

raw_G = '''
    A

    B

    C       D                   E
                    F


                    G
         H
         
        I                   




                            J   
'''

G = {}
for i, line in enumerate(raw_G.split('\n')):
    for j, c in enumerate(line):
        if c != ' ':
            G[c] = (j,i)

def dist(a,b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    return sqrt(dx**2 + dy**2)

def cost(pos):
    return sum(dist(a,b) for a,b in zip(pos[:-1], pos[1:]))

def pos(sol):
    return [G[x] for x in sol]

def P(t, c):
    return e**(-c / t) if c > 0 else 1

def accept(t, dc):
    return random() <= P(t,dc)

def swaps(sol):
    for i in range(len(sol)):
        for j in range(i+1, len(sol)):
            sol_copy = [x for x in sol]
            sol_copy[i], sol_copy[j] = sol_copy[j], sol_copy[i]
            yield sol_copy

def dc(A, B):
    return cost(pos(B)) - cost(pos(A))


if __name__ == '__main__':
    sol = [key for key in G.keys()]
    print('Initial:', sol, cost(pos(sol)))
    
    for t in range(1000, 0, -1):
        for swap in swaps(sol):
            if accept(t, dc(sol, swap)):
                sol = swap
                continue

    print('After SA:', sol, cost(pos(sol)))
