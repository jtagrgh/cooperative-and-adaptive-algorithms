from math import sqrt
from itertools import permutations

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

def pos(sol):
    return [G[x] for x in sol]

def cost(sol):
    return sum(dist(a,b) for a,b in zip(pos(sol)[:-1], pos(sol)[1:]))

tabu_list = [[0 for _ in range(10)] for _ in range(10)]
tabu_tenure = sqrt(10)
sol = [key for key in G.keys()]
best_cost = cost(sol)

def swap(i,j):
    sol[i], sol[j] = sol[j], sol[i]

def is_not_tabu(i,j):
    return tabu_list[i][j] == 0

def update_tabu_list():
    for row in tabu_list:
        for i in range(len(row)):
            if row[i] > 0:
                row[i] -= 1

def make_tabu(i,j):
    tabu_list[i][j] = tabu_tenure

def do_best_swap():
    global best_cost
    best_swap_pair = (None, None)
    best_swap_cost = float('inf')
    found_better = False
    for i in range(len(sol)):
        for j in range(i+1, len(sol)):
            swap(i,j)
            c = cost(sol)
            if c < best_swap_cost and (is_not_tabu(i,j) or c < best_cost):
                best_swap_pair = (i,j)
                best_swap_cost = c
                found_better = True
            swap(i,j)
    if found_better:
        i,j = best_swap_pair
        swap(i,j)
        make_tabu(i,j)
        if best_swap_cost < best_cost:
            best_cost = best_swap_cost

def brute_force():
    base_sol = sorted(key for key in G.keys())
    print(min(cost(sol) for sol in permutations(base_sol, len(base_sol))))
    # 55.15435450860047

if __name__ == '__main__':
    print('Initial:', sol, cost(sol))

    for i in range(100):
        update_tabu_list()
        do_best_swap()

    print('After:', sol, best_cost)

