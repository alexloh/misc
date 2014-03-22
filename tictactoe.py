# Ultimate Tic-tac-toe frontend and AI

from numpy import *

class GameState:
  color = 1
  currentBig = None
  state = zeros((9,9))
  bigState = zeros((3,3))

  def __init__(self):
    pass

  def checkWin(self):
    pass

  # current tuple representing which big square is playable
  # return None if all squares are playable
  def currentBig(self):
    return self.currentBig

  # make a move by specifying the big square first then the little one
  def move(self, bigx, bigy, smallx, smally):
    move(self, bigx*3+smallx, bigy*3+smally)

  # make a move by specifying the actual coordinates on the 9x9 board
  def move(self, x, y):
    self.state[x][y] = self.color
    self.flipTurn()

  def flipTurn(self):
    self.color = 1 if self.color == 2 else 2

  '''
    X O  |     |
  2   O  |  O  |
      O X|     |
    -----+-----+-
         |     |
      A     B     C
  '''
  def render(self):
    #map everything to a bitmap first then print that array
    bitmap = [[' ' for x in range(19)] for y in range(12)]
    # grid
    for x in range(2):
      for y in range(17):
        bitmap[x*4+3][y+2] = '-'
    for x in range(2):
      for y in range(11):
        bitmap[y][x*6+7] = '|'
    # legend
    bitmap[1][0] = '3'
    bitmap[5][0] = '2'
    bitmap[9][0] = '1'
    bitmap[11][4] = 'A'
    bitmap[11][10] = 'B'
    bitmap[11][16] = 'C'
    #print the bitmap
    for y in range(12):
      print ''.join(bitmap[y])
    pass

class GUI:
  def main(self, game):
    while True:
      color1 = 'O' if game.color==1 else 'X'
      print "\n\n"
      game.render()
      print "======================================"
      print color1+" to move:"
      
      move = input("Move for "+color1+"? ")
      x = ord(move[0]) - ord('A')
      y = ord(move[1]) - ord('0')
      game.move(x,y)

class AI:
  pass


gui = GUI()
gui.main(GameState())

