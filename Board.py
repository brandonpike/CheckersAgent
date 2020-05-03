import copy as copy
import GUI as gui

class Board():
	def __init__(self):
		self.board = [[0,1,0,1,0,1,0,1],
					  [1,0,1,0,1,0,1,0],
					  [0,1,0,1,0,1,0,1],
					  [0,0,0,0,0,0,0,0],
					  [0,0,0,0,0,0,0,0],
					  [-1,0,-1,0,-1,0,-1,0],
					  [0,-1,0,-1,0,-1,0,-1],
					  [-1,0,-1,0,-1,0,-1,0]]
		'''self.board = [[0,1,0,1,0,1,0,1],
					  [1,0,1,0,1,0,1,0],
					  [0,1,0,1,0,1,0,1],
					  [0,0,0,0,0,0,0,0],
					  [0,0,0,0,0,0,0,0],
					  [-1,0,-1,0,-1,0,-1,0],
					  [0,1,0,-1,0,-1,0,-1],
					  [0,0,0,0,-1,0,-1,0]]'''
		self.white_pieces = 12
		self.black_pieces = 12
		self.playing = True
		self.mustHop = False
		self.mustHopPiece = None
		self.moves_made = 0
		self.pyBoard = []
		self.turn = 1
		# Gui test
		self.clearMarkings = False
		self.printed = False
		self.curBegin = None
		self.curEnd = None

	def clearMarks(self):
		if self.curBegin:
			self.pyBoard[int(self.curBegin[0])][int(self.curBegin[2])].chosen = False
			self.pyBoard[int(self.curBegin[0])][int(self.curBegin[2])].status = False
		self.curBegin = None
		if self.curEnd:
			self.pyBoard[int(self.curEnd[0])][int(self.curEnd[2])].chosen = False
			self.pyBoard[int(self.curEnd[0])][int(self.curEnd[2])].status = False
		self.curEnd = None
		for i,row in enumerate(self.pyBoard):
			for j,col in enumerate(row):
				col.status = False
				col.chosen = False

	def checkClicks(self):
		for i,row in enumerate(self.pyBoard):
			for j,col in enumerate(row):
				if not self.clearMarkings and col.status:
					s = str(i)+","+str(j)
					if self.curBegin and s != self.curBegin:
						self.pyBoard[int(self.curBegin[0])][int(self.curBegin[2])].chosen = False
						self.curEnd = s
					else:
						col.chosen = True
						self.curBegin = s
					col.status = False
				elif self.clearMarkings:
					self.clearMarks()
					self.clearMarkings = False

	def printBoard(self):
		if len(self.pyBoard) == 0:
			y = 20 # +55
			for i,row in enumerate(self.board):
				x = 35 # +80
				pyrow = []
				for j,col in enumerate(row):
					pyrow.append(gui.createButton(str(col), x, y, 80, 55, (255,255,255), (249,249,97)))
					x += 80
				y += 55
				self.pyBoard.append(pyrow)
		else:
			for row in self.pyBoard:
				for col in row:
					col.update()

	def removePiece(self, piece):
		if self.board[piece[0]][piece[1]] == 0:
			return False
		else:
			if self.board[piece[0]][piece[1]] < 0:
				self.black_pieces -= 1
				if self.black_pieces == 0:
					self.playing = False
					self.winner = 1
			elif self.board[piece[0]][piece[1]] > 0:
				self.white_pieces -= 1
				if self.white_pieces == 0:
					self.playing = False
					self.winner = -1
			self.board[piece[0]][piece[1]] = 0
			self.pyBoard[piece[0]][piece[1]].text = str(0)

	def makeMove(self, begin, end):

		col_diff = end[1]-begin[1]
		row_diff = end[0]-begin[0]

		if self.mustHop and abs(col_diff) == 1:
			print("a")
			return False
		elif self.mustHop and begin != self.mustHopPiece:
			print("b")
			return False
		elif not self.mustHop and begin == end:
			print("c")
			return False

		if begin == end:
			self.mustHop = False
			self.mustHopPiece = None
			self.turn *= -1

		moveAble = (1,2) if self.turn == 1 else (-1,-2)
		if self.board[begin[0]][begin[1]] not in moveAble:
			return False

		isValid = self.checkMove(begin,end)
		if isValid:
			endings = {-1:0,1:7}
			if endings[self.turn] == end[0]:
				self.board[begin[0]][begin[1]] = 2*self.turn
			self.board[end[0]][end[1]] = self.board[begin[0]][begin[1]]
			self.board[begin[0]][begin[1]] = 0
			self.pyBoard[begin[0]][begin[1]].text = str(0)
			self.pyBoard[end[0]][end[1]].text = str(self.board[end[0]][end[1]])

			if abs(col_diff) == 2: # is hop, dont change turns
				print("is hop | ",end='')
				self.removePiece((begin[0]+int(row_diff/2),begin[1]+int(col_diff/2)))
				self.mustHop = True
				self.mustHopPiece = end
			else:
				self.turn *= -1
			print("Move made -", begin,"->",end)
			self.printed = False
			self.moves_made += 1
			return True
		else:
			print("Invalid move")
		return False

	def checkMove(self, begin,end):
		if end[0] >= 0 and end[0] < 8 and end[1] >= 0 and end[1] < 8:
			if abs(self.board[begin[0]][begin[1]]) == 2:
				return (True if end in self.getSuccessorsQueen(begin) else False)
			if self.turn == 1:
				return (True if end in self.getSuccessorsWhite(begin) else False)
			else:
				return (True if end in self.getSuccessorsBlack(begin) else False)
		else:
			return False

	#def isHop(self,begin,end):

	# ARCHIVED #
	'''def getPath(self, begin, end):
		# Check path
		if self.board[begin[0]][begin[1]] == 1: # if white turn
			sucessorFunc = "getSuccessorsWhite"
		elif self.board[begin[0]][begin[1]] == -1: # if black turn
			sucessorFunc = "getSuccessorsBlack"
		elif self.board[begin[0]][begin[1]] in (-2,2): # if queen
			sucessorFunc = "getSuccessorsQueen"
		func = 'self.'+sucessorFunc+'('+str(begin)+','+str(True)+')' # Can do dist=1 or dist=2

		path = [begin]
		Q = [begin]
		flag = True
		while len(Q) > 0:
			print("Next",str(Q))
			n = Q.pop()
			if n == end:
				print("FOUND")
				return path 

			successors = eval('self.'+sucessorFunc+'('+str(n)+','+str(flag)+')')
			flag = False
			for s in successors:
				if abs(s[0]-n[0]) == 1 and abs(s[1]-n[1]) == 1:
					print(s,1)
					if s == end:
						return path + [s]
				else:
					Q.append(s)

		return False'''

	def getSuccessorsWhite(self, point):
		#print("WHITE SUCCESSORS",point)
		successors = []
		# DL or DR
		if point[0]+1 < 8: # row index check
			# DR
			if not self.mustHop and point[1]+1 < 8 and self.board[point[0]+1][point[1]+1] == 0: # Dist=1
				successors.append((point[0]+1,point[1]+1))
			else: # Dist=2
				if point[1]+1 < 8 and self.board[point[0]+1][point[1]+1] in (-1,-2): # Black piece we can hop
					if point[0]+2 < 8 and point[1]+2 < 8 and self.board[point[0]+2][point[1]+2] == 0: # Hoppable
						successors.append((point[0]+2,point[1]+2))
			# DL
			if not self.mustHop and point[1]-1 >= 0 and self.board[point[0]+1][point[1]-1] == 0: # Dist=1
				successors.append((point[0]+1,point[1]-1))
			else: # Dist=2
				if point[1]-1 >= 0 and self.board[point[0]+1][point[1]-1] in (-1,-2): # Black piece we can hop
					if point[0]+2 < 8 and point[1]-2 >= 0 and self.board[point[0]+2][point[1]-2] == 0: # Hoppable
						successors.append((point[0]+2,point[1]-2))
		return successors

	def getSuccessorsBlack(self, point):
		#print("BLACK SUCCESSORS",point)
		successors = []
		# UL or UR
		if point[0]-1 >= 0: # row index check
			# UR
			if not self.mustHop and point[1]+1 < 8 and self.board[point[0]-1][point[1]+1] == 0: # Dist=1
				successors.append((point[0]-1,point[1]+1))
			else: # Dist=2
				if point[1]+1 < 8 and self.board[point[0]-1][point[1]+1] in (1,2): # White piece we can hop
					if point[0]-2 >= 0 and point[1]+2 < 8 and self.board[point[0]-2][point[1]+2] == 0: # Hoppable
						successors.append((point[0]-2,point[1]+2))
			# UL
			if not self.mustHop and point[1]-1 >= 0 and self.board[point[0]-1][point[1]-1] == 0: # Dist=1
				successors.append((point[0]-1,point[1]-1))
			else: # Dist=2
				if point[1]-1 >= 0 and self.board[point[0]-1][point[1]-1] in (1,2): # Black piece we can hop
					if point[0]-2 >= 0 and point[1]-2 >= 0 and self.board[point[0]-2][point[1]-2] == 0: # Hoppable
						successors.append((point[0]-2,point[1]-2))
		return successors

	# Work in progress
	def getSuccessorsQueen(self, point):
		print("QUEEN SUCCESSORS",point)
		ourPiece = self.board[point[0]][point[1]]
		captureable = (-1,-2) if ourPiece == 2 else (1,2)
		print(ourPiece,captureable)
		successors = []
		# UL or UR
		if point[0]-1 >= 0: # row index check
			# UR
			if not self.mustHop and point[1]+1 < 8 and self.board[point[0]-1][point[1]+1] == 0: # Dist=1
				successors.append((point[0]-1,point[1]+1))
			else: # Dist=2
				if point[1]+1 < 8 and self.board[point[0]-1][point[1]+1] in captureable: # Opposite piece we can hop
					if point[0]-2 >= 0 and point[1]+2 < 8 and self.board[point[0]-2][point[1]+2] == 0: # Hoppable
						successors.append((point[0]-2,point[1]+2))
			# UL
			if not self.mustHop and point[1]-1 >= 0 and self.board[point[0]-1][point[1]-1] == 0: # Dist=1
				successors.append((point[0]-1,point[1]-1))
			else: # Dist=2
				if point[1]-1 >= 0 and self.board[point[0]-1][point[1]-1] in captureable: # Opposite piece we can hop
					if point[0]-2 < 8 and point[1]-2 >= 0 and self.board[point[0]-2][point[1]-2] == 0: # Hoppable
						successors.append((point[0]-2,point[1]-2))
		# DL or DR
		if point[0]+1 < 8: # row index check
			# DR
			if not self.mustHop and point[1]+1 < 8 and self.board[point[0]+1][point[1]+1] == 0: # Dist=1
				successors.append((point[0]+1,point[1]+1))
			else: # Dist=2
				if point[1]+1 < 8 and self.board[point[0]+1][point[1]+1] in captureable: # Black piece we can hop
					if point[0]+2 < 8 and point[1]+2 < 8 and self.board[point[0]+2][point[1]+2] == 0: # Hoppable
						successors.append((point[0]+2,point[1]+2))
			# DL
			if not self.mustHop and point[1]-1 >= 0 and self.board[point[0]+1][point[1]-1] == 0: # Dist=1
				successors.append((point[0]+1,point[1]-1))
			else: # Dist=2
				if point[1]-1 >= 0 and self.board[point[0]+1][point[1]-1] in captureable: # Black piece we can hop
					if point[0]+2 < 8 and point[1]-2 >= 0 and self.board[point[0]+2][point[1]-2] == 0: # Hoppable
						successors.append((point[0]+2,point[1]-2))
		print(successors)
		return successors

	def __str__(self):
		s = "Move: " + str(self.moves_made) + "\n"
		for i,row in enumerate(self.board):
			for j,col in enumerate(row):
				if col in (0,1,2):
					s += " "
				s += str(col)
				if j != len(row)-1:
					s += ","
			s += "\n"
		s += 'w:'+str(self.white_pieces)+' b:'+str(self.black_pieces) + "\n"
		return s