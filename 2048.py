from os import system, name

import unittest

def cls():
	# stolen from screen_clear from https://www.tutorialspoint.com/how-to-clear-screen-using-python
   if name == 'nt':
      _ = system('cls')
   # for mac and linux(here, os.name is 'posix')
   else:
      _ = system('clear')


def halo():
	return 'halo'

def init_board(n):
	row = [0] * n
	return [row] * n

def print_board(board, dim):
	for i in range(dim):
		row = board[i]
		print(''.join([' ' if j==0 else str(j) for j in row ]))


def move_left(board):
	d = len(board)
	for row in board:
		row = [j for j in row if j != 0]
		row = row + [0]*(d-len(row))
	return board


def main():
	dim = int(input('dimension = '))
	tgt = int(input('target score = '))

	cls()
	board = init_board(dim)
	print_board(board, dim)

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
		new_board = move_left(board)
		self.assertEqual(new_board, board)


if __name__ == '__main__':
	main()

