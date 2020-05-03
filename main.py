class Board():
	def __init__(self):
		self.board = [[1,0,1,0,1,0,1,0],
					  [0,1,0,1,0,1,0,1],
					  [1,0,1,0,1,0,1,0],
					  [0,-1,0,0,0,0,0,0],
					  [0,0,0,0,0,0,0,0],
					  [-1,-1,0,0,-1,0,-1,0],
					  [0,-1,0,-1,0,-1,0,-1],
					  [-1,0,-1,0,-1,0,-1,0]]
		'''self.board = [[1,0,1,0,1,0,1,0],
					  [0,1,0,1,0,1,0,1],
					  [1,0,1,0,1,0,1,0],
					  [0,0,0,0,0,0,0,0],
					  [0,0,0,0,0,0,0,0],
					  [-1,0,-1,0,-1,0,-1,0],
					  [0,-1,0,-1,0,-1,0,-1],
					  [-1,0,-1,0,-1,0,-1,0]]'''
		self.moves_made = 0

	def makeMove(self, begin, end):
		path = self.getPath(begin,end)
		if path:
			self.board[end[0]][end[1]] = self.board[begin[0]][begin[1]]
			self.board[begin[0]][begin[1]] = 0
			print("Move made -", begin,"->",end)
			self.moves_made += 1
			return True
		return False

	def getPath(self, begin, end):
		# Check path
		if self.board[begin[0]][begin[1]] == 1: # if white turn
			sucessorFunc = "getSuccessorsWhite"
		elif self.board[begin[0]][begin[1]] == -1: # if black turn
			sucessorFunc = "getSuccessorsBlack"
		elif self.board[begin[0]][begin[1]] in (-2,2): # if queen
			sucessorFunc = "getSuccessorsQueen"

		path = [begin]
		Q = [begin]
		while len(Q) > 0:
			print("Next",str(Q))
			n = Q.pop()
			if n == end:
				print("FOUND")
				return Q

			successors = eval('self.'+sucessorFunc+'('+str(n)+')')
			for s in successors:
				if abs(s[0]-n[0]) == 1 and abs(s[1]-n[1]) == 1:
					if s == end:
						return path + [s]
					else:
						print(s,1)
				else:
					Q.append(s)


		return False

	def getSuccessorsWhite(self, point):
		print("WHITE SUCCESSORS",point)
		# DL or DR
		successors = set()
		if point[0]+1 < 8: # row index check
			# DR
			if point[1]+1 < 8 and self.board[point[0]+1][point[1]+1] == 0: # Dist=1
				successors.add((point[0]+1,point[1]+1))
			else: # Dist=2
				if point[1]+1 < 8 and self.board[point[0]+1][point[1]+1] in (-1,-2): # Black piece we can hop
					if point[0]+2 < 8 and point[1]+2 < 8 and self.board[point[0]+2][point[1]+2] == 0: # Hoppable
						successors.add((point[0]+2,point[1]+2))
			# DL
			if point[1]-1 >= 0 and self.board[point[0]+1][point[1]-1] == 0: # Dist=1
				successors.add((point[0]+1,point[1]-1))
			else: # Dist=2
				if point[1]-1 >= 0 and self.board[point[0]+1][point[1]-1] in (-1,-2): # Black piece we can hop
					if point[0]+2 < 8 and point[1]-2 >= 0 and self.board[point[0]+2][point[1]-2] == 0: # Hoppable
						successors.add((point[0]+2,point[1]-2))
		return successors

	def getSuccessorsBlack(self, point):
		print("BLACK SUCCESSORS",point)
		successors = set()
		# UL or UR
		if point[0]-1 >= 0: # row index check
			# UR
			if point[1]+1 < 8 and self.board[point[0]-1][point[1]+1] == 0: # Dist=1
				successors.add((point[0]-1,point[1]+1))
			else: # Dist=2
				if point[1]+1 < 8 and self.board[point[0]-1][point[1]+1] in (1,2): # White piece we can hop
					if point[0]-2 >= 0 and point[1]+2 < 8 and self.board[point[0]-2][point[1]+2] == 0: # Hoppable
						successors.add((point[0]-2,point[1]+2))
			# UL
			if point[1]-1 >= 0 and self.board[point[0]-1][point[1]-1] == 0: # Dist=1
				successors.add((point[0]-1,point[1]-1))
			else: # Dist=2
				if point[1]-1 >= 0 and self.board[point[0]-1][point[1]-1] in (1,2): # Black piece we can hop
					if point[0]-2 < 8 and point[1]-2 >= 0 and self.board[point[0]-2][point[1]-2] == 0: # Hoppable
						successors.add((point[0]-2,point[1]-2))
		return successors

	def getSuccessorsQueen(self, point):
		print("QUEEN SUCCESSORS",point)
		ourPiece = self.board[point[0]][point[1]]
		captureable = (-1,-2) if ourPiece == 2 else (1,2)
		print(ourPiece,captureable)
		successors = set()
		# UL or UR
		if point[0]-1 >= 0: # row index check
			# UR
			if point[1]+1 < 8 and self.board[point[0]-1][point[1]+1] == 0: # Dist=1
				successors.add((point[0]-1,point[1]+1))
			else: # Dist=2
				if point[1]+1 < 8 and self.board[point[0]-1][point[1]+1] in captureable: # Opposite piece we can hop
					if point[0]-2 >= 0 and point[1]+2 < 8 and self.board[point[0]-2][point[1]+2] == 0: # Hoppable
						successors.add((point[0]-2,point[1]+2))
			# UL
			if point[1]-1 >= 0 and self.board[point[0]-1][point[1]-1] == 0: # Dist=1
				successors.add((point[0]-1,point[1]-1))
			else: # Dist=2
				if point[1]-1 >= 0 and self.board[point[0]-1][point[1]-1] in captureable: # Opposite piece we can hop
					if point[0]-2 < 8 and point[1]-2 >= 0 and self.board[point[0]-2][point[1]-2] == 0: # Hoppable
						successors.add((point[0]-2,point[1]-2))
		# DL or DR
		if point[0]+1 < 8: # row index check
			# DR
			if point[1]+1 < 8 and self.board[point[0]+1][point[1]+1] == 0: # Dist=1
				successors.add((point[0]+1,point[1]+1))
			else: # Dist=2
				if point[1]+1 < 8 and self.board[point[0]+1][point[1]+1] in captureable: # Opposite piece we can hop
					if point[0]+2 < 8 and point[1]+2 < 8 and self.board[point[0]+2][point[1]+2] == 0: # Hoppable
						successors.add((point[0]+2,point[1]+2))
			# DL
			if point[1]-1 >= 0 and self.board[point[0]+1][point[1]-1] == 0: # Dist=1
				successors.add((point[0]+1,point[1]-1))
			else: # Dist=2
				if point[1]-1 >= 0 and self.board[point[0]+1][point[1]-1] in captureable: # Opposite piece we can hop
					if point[0]+2 < 8 and point[1]-2 >= 0 and self.board[point[0]+2][point[1]-2] == 0: # Hoppable
						successors.add((point[0]+2,point[1]-2))
		return successors

	def __str__(self):
		s = "Move: " + str(self.moves_made) + "\n"
		for i,row in enumerate(self.board):
			for j,col in enumerate(row):
				s += str(col)
				if j != len(row)-1:
					s += ","
			s += "\n"
		return s

def main():
	board = Board()
	print(board)
	begin = (2,2)
	end = (6,2)
	print(board.getPath(begin,end))
	#print(str(board.makeMove((0,0), (4,1))) + "\n")
	#print(board)

if __name__ == '__main__':
	main()