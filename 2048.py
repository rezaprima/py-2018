from os import system, name

def cls():
	# stolen from screen_clear from https://www.tutorialspoint.com/how-to-clear-screen-using-python
   if name == 'nt':
      _ = system('cls')
   # for mac and linux(here, os.name is 'posix')
   else:
      _ = system('clear')


dim = int(input('dimension = '))
tgt = int(input('target score = '))

cls()
print(dim, tgt)