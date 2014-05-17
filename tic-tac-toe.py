#coding:utf-8
"""
	Use min-max algorithm with alpha-beta prune
	simple tic-tok game
	author: Sunny Song
	email: songbo.sunny@gmail.com
	last updated: 5/17/2014
"""
import time
import sys
from sys import stdout

class _Getch:
	def __init__(self):
		self.impl = _GetchWindows()
	def __call__(self): return self.impl()
class _GetchWindows:
	def __init__(self):
		import msvcrt
	def __call__(self):
		import msvcrt
		return msvcrt.getch()

class TileState:
	EMPTY = 0
	CIRCLE = 1
	CROSS = 2

class Board:
	SIZE = 3

class Mode:
	CIRCLE = 1
	CROSS = 2

class State:
	FULL = 0
	CROSS_WIN = 1
	CIRCLE_WIN = 2
	NOTFULL = 3

def print_board(board):
	print ""
	for i in range(Board.SIZE**2):
		if board[i] == TileState.EMPTY:
			stdout.write("   ")
		elif board[i] == TileState.CIRCLE:
			stdout.write(" 0 ")
		elif board[i] == TileState.CROSS:
			stdout.write(" X ")
		if (i+1) % Board.SIZE == 0:# a new line
			if (i+1) != Board.SIZE**2: # not the last line
				print ""
				for r in range(Board.SIZE):
					stdout.write("--- ")
				print ""
		else:
			stdout.write("|")
	print ""

def checkState(board):
	
	isFull = True
	crossWin = [True]*(Board.SIZE*2+2)
	circleWin = [True]*(Board.SIZE*2+2)
	for i in range(Board.SIZE):
		if board[i*Board.SIZE+i] != TileState.CROSS:
			crossWin[Board.SIZE*2] = False
		if board[i*Board.SIZE+i] != TileState.CIRCLE:
			circleWin[Board.SIZE*2] = False
		if board[i*Board.SIZE+Board.SIZE-i-1] != TileState.CROSS:
			crossWin[Board.SIZE*2+1] = False
		if board[i*Board.SIZE+Board.SIZE-i-1] != TileState.CIRCLE:
			circleWin[Board.SIZE*2+1] = False
		for j in range(Board.SIZE):
			if board[i*Board.SIZE+j] == TileState.EMPTY:
				isFull = False
			if board[i*Board.SIZE+j] != TileState.CROSS:
				crossWin[i] = crossWin[Board.SIZE+j] = False

			if board[i*Board.SIZE+j] != TileState.CIRCLE:
				circleWin[i] = circleWin[Board.SIZE+j] = False

	for c in crossWin:
		if c == True:
			return State.CROSS_WIN
	for c in circleWin:
		if c == True:
			return State.CIRCLE_WIN
	if isFull:
		return State.FULL
	else:
		return State.NOTFULL

	if isFull == True:
		return State.FULL
	else:
		return State.NOTFULL

def move(board):
	state = checkState(board)

	if state != State.NOTFULL:
		return state
	maxp = -1
	nextstep = 0
	beta=100	
	for i in range(Board.SIZE**2):
		alpha = -1		
		if board[i] == TileState.EMPTY:
			newboard = board[:]
			newboard[i] = Mode.CROSS			
			p = minMaxSearch(newboard,Mode.CIRCLE, alpha, beta)
			
			if p > maxp:
				maxp = p
				nextstep = i
	board[nextstep] = Mode.CROSS
	return checkState(board)

#return possiblity of crosswin under current situation
def minMaxSearch(board, mode, alpha, beta):
	state = checkState(board)
	if state == State.CROSS_WIN:
		return 1
	elif state == State.CIRCLE_WIN:
		return 0
	elif state == State.FULL:
		return 0.1 # ?
	partialPossibility = []
	fatherBeta = beta
	if mode == Mode.CIRCLE:
		newmode = Mode.CROSS
	else:
		newmode = Mode.CIRCLE
	maxp = -1 #initial eval in max node, negative infinite
	minp = 100 # initial eval in min node, positive infinite
	for i in range(Board.SIZE**2):
		tile = board[i]
		if tile == TileState.EMPTY:
			newboard = board[:]
			newboard[i] = mode
			p = minMaxSearch(newboard, newmode, alpha, beta)

			if mode == Mode.CROSS: # max node
				if p >= maxp:
					maxp = p

					if maxp > alpha:
						alpha = maxp

					if maxp > fatherBeta: # if eval in max node bigger than beta of its father node
						return maxp		# return

			elif mode == Mode.CIRCLE: # min node
				if p <= minp:
					minp = p
					beta = minp #update beta of this node
					if minp < alpha:
						return minp


	if mode == Mode.CROSS: #max node
		return maxp
	elif mode == Mode.CIRCLE: # min node				
		return minp
	else:
		print "impossible"


def main():
	
	board = [TileState.EMPTY]*Board.SIZE**2
	getch = _Getch()
	print_board(board)
	while True:
		try:
			char = getch()
			c = int(char)
			if c <= 0 or c > Board.SIZE**2:
				raise ValueError
		except ValueError:
			if ord(char) == 3: #ctrl + c
				break
			else:
				print "Please make a move by entering a number between %d and %d" %(1,Board.SIZE**2)
				continue
		c = c - 1
		if c >= 6:
			c = c - 6
		elif c <= 2:
			c = c + 6
		if board[c] == TileState.EMPTY:
			board[c] = TileState.CIRCLE
		else:
			print "The move is illegal"
			continue
		print_board(board)
		state = move(board)
		print_board(board)
		if state == State.CIRCLE_WIN:
			print "You WIN"
			break
		elif state == State.CROSS_WIN:
			print "You LOSE"
			break
		elif state == State.FULL:
			print "Draw"
			break

if __name__ == "__main__":
		main()
