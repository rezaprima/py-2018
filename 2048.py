from os import system, name

import unittest
import random

def cls():
	# stolen from screen_clear from https://www.tutorialspoint.com/how-to-clear-screen-using-python
   if name == 'nt':
      _ = system('cls')
   # for mac and linux(here, os.name is 'posix')
   else:
      _ = system('clear')

# stolen from https://stackoverflow.com/a/21659588
def _find_getch():
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch

    # POSIX system. Create and return a getch that manipulates the tty.
    import sys, tty
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    return _getch

getch = _find_getch()

def halo():
	return 'halo'

def init_board(n):
	board = []
	row = [0] * n
	for i in range(n):
		board.append(row[:])
	return board

def print_board(board):
	for i in range(len(board)):
		row = board[i]
		print('|'+'|'.join(['    ' if j==0 else f"{j:>4}" for j in row ])+'|')


def move_left(board):
	d = len(board)
	new_board = []
	for row in board:
		new_row = [j for j in row if j != 0]
		new_row = new_row + [0]*(d-len(new_row))
		new_board.append(new_row)
	return merge_left(new_board)

def move_right(board):
	d = len(board)
	new_board = []
	for row in board:
		new_row = [j for j in row if j != 0]
		new_row = [0]*(d-len(new_row)) + new_row
		new_board.append(new_row)
	return merge_right(new_board)

def transpose(board):
	return [list(c) for c in zip(*board)]


def move_top(board):
	return transpose(move_left(transpose(board)))

def move_bottom(board):
	return transpose(move_right(transpose(board)))


def merge_left(board):
	new_board = []
	for row in board:
		new_row = merge_row_left(row)
		new_board.append(new_row)
	return new_board

def merge_right(board):
	new_board = []
	for row in board:
		new_row = merge_row_right(row)
		new_board.append(new_row)
	return new_board

def merge_row_left(row):
	d = len(row)
	last = 0
	for i in range(d):
		cell = row[i]
		if(last!=0 and last==cell):
			row[i-1]=2*cell
			row[i] = 0
		last = row[i]
	new_row = [j for j in row if j!=0]
	return new_row + [0]*(d-len(new_row))

def merge_row_right(row):
	row_copy = row[:]
	row_copy.reverse()
	merged = merge_row_left(row_copy)
	merged.reverse()
	return merged 

def target_achieved(board, tgt):
	return any(c >= tgt for r in board for c in r)

def seed_board(board, count):
	i=0
	while i<count:
		random.seed()
		r = random.randrange(0,len(board))
		random.seed()
		c = random.randrange(0,len(board))
		if(board[r][c]!=0):
			continue
		board[r][c]=2
		i=i+1
	return board

def no_more_move(board):
	return not any(c==0 for r in board for c in r)


def main():
	# dim = int(input('dimension = '))
	# tgt = int(input('target score = '))
	dim,tgt = 4,16

	cls()
	board = init_board(dim)
	board = seed_board(board, 2)
	print_board(board)

	while True:
		a = getch()
		if(a=='a'):
			new_board = move_left(board)
		elif(a=='d'):
			new_board = move_right(board)
		elif(a=='w'):
			new_board = move_top(board)
		elif(a=='s'):
			new_board = move_top(board)

		new_board = seed_board(new_board, 1)
		cls()
		print_board(new_board)
		board = new_board
		if(target_achieved(board, tgt)):
			print("YOU WON")
			break

		if(no_more_move(board)):
			print("YOU LOSE")
			break



class TestBoard(unittest.TestCase):
	def test_truth(self):
		h = halo()
		self.assertEqual('halo', h)


	def test_board(self):
		board = [
		[2,0,0,0],
		[0,2,0,0],
		[0,0,2,0],
		[0,0,0,2]
		]
		new_board = [
		[2,0,0,0],
		[0,2,0,0],
		[0,0,2,0],
		[0,0,0,2]
		]
		self.assertEqual(new_board, board)


	def test_move_left(self):
		board = [
		[2,0,0,0],
		[0,2,0,0],
		[0,0,2,0],
		[0,0,0,2]
		]
		new_board = [
		[2,0,0,0],
		[2,0,0,0],
		[2,0,0,0],
		[2,0,0,0],
		]
		self.assertEqual(new_board, move_left(board))

	def test_move_right(self):
		board = [
		[2,0,0,0],
		[0,2,0,0],
		[0,0,2,0],
		[0,0,0,2]
		]
		new_board = [
		[0,0,0,2],
		[0,0,0,2],
		[0,0,0,2],
		[0,0,0,2],
		]
		self.assertEqual(new_board, move_right(board))

	def test_move_top(self):
		board = [
		[2,0,0,0],
		[0,2,0,0],
		[0,0,2,0],
		[0,0,0,2]
		]
		new_board = [
		[2,2,2,2],
		[0,0,0,0],
		[0,0,0,0],
		[0,0,0,0],
		]
		self.assertEqual(new_board, move_top(board))

	def test_move_bottom(self):
		board = [
		[2,0,0,0],
		[0,2,0,0],
		[0,0,2,0],
		[0,0,0,2]
		]
		new_board = [
		[0,0,0,0],
		[0,0,0,0],
		[0,0,0,0],
		[2,2,2,2],
		]
		self.assertEqual(new_board, move_bottom(board))

	def test_transpose(self):
		board = [
		[2,2,2,2],
		[0,0,0,2],
		[0,0,0,2],
		[0,0,0,2]
		]
		new_board = [
		[2,0,0,0],
		[2,0,0,0],
		[2,0,0,0],
		[2,2,2,2],
		]
		self.assertEqual(new_board, transpose(board))

	def test_row_merge_left(self):
		self.assertEqual([4,0,0,0], merge_row_left([2,2,0,0]))
		self.assertEqual([4,2,0,0], merge_row_left([2,2,2,0]))
		self.assertEqual([4,4,0,0], merge_row_left([2,2,2,2]))

	def test_merge_left(self):
		board = [
		[2,0,2,0],
		[0,2,0,0],
		[0,0,2,0],
		[0,0,0,2]
		]
		new_board = [
		[4,0,0,0],
		[2,0,0,0],
		[2,0,0,0],
		[2,0,0,0],
		]
		self.assertEqual(new_board, move_left(board))

	def test_merge_right(self):
		board = [
		[2,0,2,0],
		[0,2,0,0],
		[0,0,2,0],
		[0,0,0,2]
		]
		new_board = [
		[0,0,0,4],
		[0,0,0,2],
		[0,0,0,2],
		[0,0,0,2],
		]
		self.assertEqual(new_board, move_right(board))

	def test_merge_top(self):
		board = [
		[2,0,0,0],
		[0,2,0,2],
		[2,0,2,0],
		[0,2,0,2]
		]
		new_board = [
		[4,4,2,4],
		[0,0,0,0],
		[0,0,0,0],
		[0,0,0,0],
		]
		self.assertEqual(new_board, move_top(board))

	def test_merge_bottom(self):
		board = [
		[2,0,0,2],
		[0,2,0,0],
		[2,0,2,0],
		[0,2,0,2]
		]
		new_board = [
		[0,0,0,0],
		[0,0,0,0],
		[0,0,0,0],
		[4,4,2,4],
		]
		self.assertEqual(new_board, move_bottom(board))

	def test_target_achieved(self):

		board = [
		[0,0,0,0],
		[0,0,0,0],
		[0,0,0,0],
		[4,8,2,4],
		]
		self.assertTrue(target_achieved(board, 8))

	def test_seed_board(self):
		board = [
		[0,0,0,0],
		[0,0,0,0],
		[0,0,0,0],
		[0,0,0,0],
		]
		new_board = seed_board(board, 2)
		self.assertEqual(2, len([c for r in board for c in r if c!=0]))



if __name__ == '__main__':
	main()

