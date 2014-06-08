# Ultimate Tic-tac-toe frontend and AI

#from numpy import *
from termcolor import colored

class GameState:

  # whose turn is it
  turn = 1

  # current tuple representing which big square is playable
  # return None if all squares are playable
  currentBig = None

  # state of all small boards as an amalgamated 9x9
  state = [[0 for x in range(9)] for y in range(9)]

  # state of big board as a 3x3. Derivable from state
  bigState = [[0 for x in range(3)] for y in range(3)]

  def __init__(self):
    pass

  # make a move by specifying the big square first then the little one
  def move4(self, bigx, smallx, bigy, smally):
    x = bigx*3 + smallx
    y = bigy*3 + smally
    big = (bigx, bigy)
    small = (smallx, smally)
    if (self.currentBig!=None) and (big != self.currentBig):
      return "Illegal move! Wrong small board"
    self.state[x][y] = self.turn
    win = self.checkWinSmall(big, (x,y))
    if win != None:
      self.bigState[x/3][y/3] = win
    self.turn = 1 if self.turn == 2 else 2
    self.currentBig = small

  def checkWin3x3(self, board, move=None):
    x = move[0]; y = move[1]
    #check horizontal
    if board[0][y] == board[1][y] == board[2][y]:
      return board[0][y]
    #check vertical
    if board[x][0] == board[x][1] == board[x][2]:
      return board[x][0]
    #check diagonal
    if board[0][0] == board[1][1] == board[2][2]:
      return board[0][0]
    if board[0][2] == board[1][1] == board[2][0]:
      return board[0][2]
    return None

  def checkWinBig(self, move=None):
    bigmove = (move[0] / 3, move[1] / 3)
    return self.checkWin3x3(bigState, bigmove)

  def checkWinSmall(self, smallboard, move=None):
    small = self.selectSmall(smallboard)
    smallmove = (move[0] % 3, move[1] % 3)
    return self.checkWin3x3(small, smallmove)

  def selectSmall(self, smallboard):
    offsetx = smallboard[0]*3
    offsety = smallboard[1]*3
    return [self.state[offsetx+0][offsety:offsety+3], 
            self.state[offsetx+1][offsety:offsety+3], 
            self.state[offsetx+2][offsety:offsety+3]]

  # return list of legal moves from current state
  def legalNext(self):
    pass

  # return list of legal moves that could have led to current state
  # basically any empty square on the currentBig small board
  def legalPrev(self):
    pass

  def color(self, turn):
    if turn == 1:
      return 'O'
    elif turn == 2:
      return 'X'
    return ' '

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
    bitmap[1][0] = 'C'
    bitmap[5][0] = 'B'
    bitmap[9][0] = 'A'
    bitmap[11][4] = 'A'
    bitmap[11][10] = 'B'
    bitmap[11][16] = 'C'
    # O's and X's
    for x in range(9):
      for y in range(9):
        bitmap[10 - y - (y/3)][x * 2 + 2] = self.color(self.state[x][y])
    # big state
    for bigx in range(3):
      for bigy in range(3):
        color = self.color(self.bigState[bigx][bigy])
        x = (bigx*3) * 2 + 2
        y = 10 - (bigy*3) - bigy - 2
        if color == 'O':
          bitmap[y+1][x+1] = color
          bitmap[y+1][x+3] = color
        if color == 'X':
          bitmap[y+0][x+1] = color
          bitmap[y+0][x+3] = color
          bitmap[y+2][x+1] = color
          bitmap[y+2][x+3] = color

    #print the bitmap
    bigC = ""
    if self.currentBig != None:
      bigC = " at ("+chr(self.currentBig[0]+ord('A'))+", "+chr(self.currentBig[1]+ord('A'))+")"
    print(self.color(self.turn)+" to play"+bigC)
    for y in range(12):
      print("".join(bitmap[y]))
    pass

class GUI:
  def main(self, game):

    moves = ['B2B2','B3B3','C2C2','B3B1','C2A2','B3B2']
    while True:
      print("\n")
      game.render()
      print("======================================")
      print(str(game.color(game.turn))+" to move:")
      
#      move = input("Move for "+color1+"? ")
#      print(move)
#      x = ord(move[0]) - ord('A')
#      y = ord(move[1]) - ord('0')
#      print(x,y)

      if len(moves) == 0:
        break
      move = moves[0]
      moves = moves[1:]
      print(move)
      bigx   = ord(move[0]) - ord('A')
      smallx = ord(move[1]) - ord('1')
      bigy   = ord(move[2]) - ord('A')
      smally = ord(move[3]) - ord('1')
      move = game.move4(bigx, smallx, bigy, smally)
      if move:
        print move

class AI:

  #Basic minimax algorithm
  # 1) randomly generate move
  # 2) check if 
  pass

gui = GUI()
gui.main(GameState())

