from Board import Board
from random import randint
from random import seed

# Agent always black (-1)
class Agent:
	def __init__(self):
		seed(1)
		self.myPieces = []

	def evaluate(self, piece, choices):
		# returns a dict {maxValue:index}
		value = {}
		for i,choice in enumerate(choices):
			val = 0
			if abs(choice[1]-piece[1]) == 2:
				val = 1
			value[val] = i

		return value

	def getMaxValueChoice(self, values):
		max_ = -99999
		index = None
		for i,v in enumerate(values):
			if len(v) == 0:
				continue
			maxv = max(v, key=int)
			if maxv > max_:
				max_ = maxv
				index = i
		return max_,index

	def chooseMove(self, board):
		self.getMyPieces(board)
		print("Pieces:",len(self.myPieces),end=" | ")
		#print(self.myPieces)
		moves = [board.getSuccessorsBlack(piece) for piece in self.myPieces]
		values = [self.evaluate(piece, choices) for piece,choices in zip(self.myPieces,moves)] # list of dicts {maxValue:index},{maxValue:index}
		if board.mustHop:
			moves = [board.getSuccessorsBlack(board.mustHopPiece) + [board.mustHopPiece]]
			values = [self.evaluate(board.mustHopPiece,moves[0])]
		print("Moves:",len(moves),end=" | ")
		print("Values:",len(values),end=" | ")
		max_,index = self.getMaxValueChoice(values)
		if index == None:
			return "forfeit"
		begin = self.myPieces[index] if not board.mustHop else board.mustHopPiece
		end = moves[index][values[index][max_]]
		#print(begin,end)
		begin_s = str(begin).replace("(","").replace(")","").replace(" ","")
		end_s = str(end).replace("(","").replace(")","").replace(" ","")
		s = str(begin_s) + " " + (end_s)
		#print(s)
		self.myPieces.remove(begin)
		self.myPieces.append(end)
		return s

	def getMyPieces(self,board):
		self.myPieces.clear()
		for i,row in enumerate(board.board):
			for j,col in enumerate(row):
				if col in (-1,-2):
					self.myPieces.append((i,j))
