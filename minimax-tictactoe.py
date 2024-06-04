class Game:
	board = [[-1 for _ in range(3)] for _ in range(3)]

	def move(self, who, where):
		self.board[where[1]][where[0]] = who

	def unmove(self, who, where):
		self.board[where[1]][where[0]] = -1

	def free_lines(self, who):
		opp = not who
		count = 0
		for row in self.board:
			count += all(c != opp for c in row)
		for col in zip(*self.board):
			count += all(c != opp for c in col)

		count += all(c != opp for c in (row[x] for row,x in zip(self.board, (range(len(self.board))))))
		count += all(c != opp for c in (row[x-1] for row,x in zip(self.board, (range(len(self.board), 0, -1)))))

		return count

	def win(self, who):
		for row in self.board:
			if all(c == who for c in row):
				return True
		for col in zip(*self.board):
			if all(c == who for c in col):
				return True

		if all(c == who for c in (row[x] for row,x in zip(self.board, (range(len(self.board)))))):
			return True

		if all(c == who for c in (row[x-1] for row,x in zip(self.board, (range(len(self.board), 0, -1))))):
			return True

		return False

	def open_moves(self):
		for y in range(len(self.board)):
			for x in range(len(self.board[0])):
				if self.board[y][x] == -1:
					yield (x,y)

	def print_board(self):
		for y in range(len(self.board)):
			print('|', end='')
			for x in range(len(self.board[0])):
				val = self.board[y][x]
				print(f' {val if val != -1 else ' '} ', end='|')
			print()
		print()


class Search:
	def __init__(self, game, max_depth, heuristic, who):
		self.game = game
		self.max_depth = max_depth
		self.heuristic = heuristic
		self.who = who

	def search(self, depth=0, maxxing=True):
		if depth == self.max_depth:
			return (self.heuristic(), None)

		player = int(self.who if maxxing else not self.who)

		best_score = -float('inf') if maxxing else float('inf')
		best_move = None

		for move in game.open_moves():
			game.move(player, move)
			child_score, _ = self.search(depth+1, not maxxing)
			is_better = lambda a,b: a > b if maxxing else a < b
			if is_better(child_score, best_score):
				best_score = child_score
				best_move = move
			game.unmove(player, move)

		return (best_score, best_move)


if __name__ == '__main__':
	game = Game()

	def heuristic():
		if game.win(0):
			return float('inf')
		elif game.win(1):
			return -float('inf')
		else:
			return game.free_lines(0)

	search = Search(game, 2, heuristic, 0)

	while True:
		try:
			move = input('Move x,y: ')
		except EOFError:
			print('Bye!')
			break 
		move = (int(move[0]), int(move[2]))
		if move not in game.open_moves():
			print('Not an open move.')
			continue

		game.move(1, move)
		game.print_board()
		if game.win(1):
			print("'1' wins.")
			break

		if len(list(game.open_moves())) == 0:
			print('Draw.')
			break

		_, opp_move = search.search()
		if opp_move == None:
			print("'1' wins.")
			break

		game.move(0, opp_move)
		game.print_board()
		if game.win(0):
			print("'0' wins.")
			break
