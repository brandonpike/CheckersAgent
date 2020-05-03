from Board import Board
from Agent import Agent
import GUI as gui

def playGame_AgentGUI(board):

	agent = Agent()
	inp = ""
	stayButton = gui.createButton("Stay",150, 545, 100, 50, (0,125,0), (50,100,0))
	quitButton = gui.createButton("Quit",550, 545, 100, 50, (225,50,0), (255,25,0))
	while board.playing:
		for event in gui.getpygame().event.get():
			if event.type == gui.getpygame().QUIT:
				board.playing = False;
				return

		gui.getScreen().fill((255,255,255))
		# Quit button
		quitButton.update()
		board.playing = not quitButton.status
		# Frame
		gui.createFrame(5,5,790,535,(0,0,0))

		board.printBoard()
		if not board.printed:
			print(board)
			board.printed = True

		if board.turn == 1: # User turn
			# Stay button
			if board.mustHop:
				stayButton.update()
				if stayButton.status:
					board.makeMove(board.mustHopPiece,board.mustHopPiece)
					board.clearMarkings = True
					board.curBegin = None
					board.curEnd = None
					stayButton.status = False
					continue
			if board.curBegin:
				#print(board.curBegin,end=" -> ")
				if board.curEnd:
					#print(board.curEnd, end="")
					p1 = board.curBegin.split(",")
					p2 = board.curEnd.split(",")
					begin = (int(p1[0]),int(p1[1]))
					end = (int(p2[0]),int(p2[1]))
					print(board.makeMove(begin,end))
					board.clearMarks()
				#print()
			board.checkClicks()
		else: # Computer turn
			move = agent.chooseMove(board)
			if move == 'forfeit':
				winner = 1
				board.playing = False
				continue
			split_points = move.split(" ")
			p1 = split_points[0].split(",")
			p2 = split_points[1].split(",")
			begin = (int(p1[0]),int(p1[1]))
			end = (int(p2[0]),int(p2[1]))
			print(board.makeMove(begin,end))

		gui.pygame.display.update()




		''' # Console Play
		while inp == "":
			inp = input("White move - (x,y) to (x,y): ") if board.turn == 1 else agent.chooseMove(board)
			if not checkInput(inp):
				print("Input two points or quit")
				inp = ""
		if inp.lower() == 'quit':
			break
		else:
			split_points = inp.split(" ")
			p1 = split_points[0].split(",")
			p2 = split_points[1].split(",")
			begin = (int(p1[0]),int(p1[1]))
			end = (int(p2[0]),int(p2[1]))
			print(board.makeMove(begin,end))
		inp = ""'''
	print(("User" if winner == 1 else "Computer") , "wins this game!")

def playGame_Agent(board):

	agent = Agent()
	inp = ""
	while board.playing:
		print(board)
		while inp == "":
			#inp = input(("White" if board.turn == 1 else "Black")+" move - (x,y) to (x,y): ")
			inp = input("White move - (x,y) to (x,y): ") if board.turn == 1 else agent.chooseMove(board)
			if not checkInput(inp):
				print("Input two points or quit")
				inp = ""
		if inp.lower() == 'quit':
			break
		else:
			split_points = inp.split(" ")
			p1 = split_points[0].split(",")
			p2 = split_points[1].split(",")
			begin = (int(p1[0]),int(p1[1]))
			end = (int(p2[0]),int(p2[1]))
			print(board.makeMove(begin,end))
		inp = ""

def playGame_2Humans(board):

	inp = ""
	while board.playing:
		print(board)
		while inp == "":
			inp = input(("White" if board.turn == 1 else "Black")+" move - (x,y) to (x,y): ")
			if not checkInput(inp):
				print("Input two points or quit")
				inp = ""
		if inp.lower() == 'quit':
			break
		else:
			split_points = inp.split(" ")
			p1 = split_points[0].split(",")
			p2 = split_points[1].split(",")
			begin = (int(p1[0]),int(p1[1]))
			end = (int(p2[0]),int(p2[1]))
			print(board.makeMove(begin,end))
		inp = ""

def checkInput(inp):
	if len(inp) != 7 and inp.lower() != "quit":
		return False
	else:
		return True
	return False

def main():
	board = Board()
	playGame_AgentGUI(board)

if __name__ == '__main__':
	main()