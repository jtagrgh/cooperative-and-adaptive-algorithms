board = [[None for _ in range(9)] for _ in range(9)]

D = {}

def in_D(x,y):
	if (x,y) not in D:
		D[(x,y)] = {n+1:0 for n in range(9)}

def print_board(marks=set()):
	for y in range(len(board)):
		for x in range(len(board[0])):
			if (x,y) in marks:
				print(f'\033[1m{board[y][x]}\033[0m', end=' ')
			elif board[y][x] == None:
				print('_', end=' ')
			else:
				print(board[y][x], end=' ')
		print()
	print()

def prop_neighbours(x,y):
	n = set()
	for i in range(len(board)):
		n.add((x,i))
	for i in range(len(board[0])):
		n.add((i,y))
	qy = (y // 3) * 3
	qx = (x // 3) * 3
	for i in range(3):
		for j in range(3):
			n.add((qx+j, qy+i))
	return n

def forward_prop(x,y, v):
	for x,y in prop_neighbours(x,y):
		in_D(x,y)
		D[(x,y)][v] -= 1

def un_prop(x,y, v):
	for x,y in prop_neighbours(x,y):
		in_D(x,y)
		D[(x,y)][v] += 1

def set_v(x,y, v):
	board[y][x] = v
	forward_prop(x,y, v)

def unset_v(x,y, v):
	board[y][x] = None
	un_prop(x,y, v)

def neighbours(x,y):
	n = []
	if x-1 >= 0:
		n.append((x-1,y))
	if x+1 < len(board[0]):
		n.append((x+1,y))
	if y-1 >= 0:
		n.append((x,y-1))
	if y+1 < len(board):
		n.append((x,y+1))
	return n

picked = set()
open_set = set((x,y) for x in range(9) for y in range(9))

def valid(x,y):
	if board[y][x] != None:
		return True
	return any(v == 0 for v in D[(x,y)].values())

def free_domain(x,y):
	return [k for k,v in D[(x,y)].items() if v == 0]

closed_set = set()
open_set = [(x,y) for x in range(9) for y in range(9)]

def open_neighbours(x,y):
	return (n for n in neighbours(x,y) if n not in closed_set)

def pick():
	x,y = open_set.pop()
	in_D(x,y)

	domain = free_domain(x,y)

	if len(open_set) == 0:
		set_v(x,y, domain[0])
		return True

	for v in domain:
		set_v(x,y, v)

		if not all(valid(px,py) for px,py in prop_neighbours(x,y)):
			unset_v(x,y, v)
			continue

		if pick():
			return True

		unset_v(x,y, v)

	open_set.append((x,y))
	return False

pick()
print_board()