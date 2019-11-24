#!/usr/bin/python3

import logging
import random
import pprint

FN = "rexbrickapy.log"
logPath = "."
logging.basicConfig(filename=FN,
                    filemode='w',
                    level=logging.DEBUG,
                    format="%(levelname)s %(asctime)s %(funcName)s @%(lineno)d %(message)s")

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()

fileHandler = logging.FileHandler("{0}/{1}".format(logPath, FN))
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

BOARD_WIDTH = 7
BOARD_HEIGHT = BOARD_WIDTH
MIDDLE = -(-BOARD_WIDTH // 2)

class Card:
    def __init__(self, lsuit, lval, rsuit, rval):
        self.left = lsuit, lval
        self.right = rsuit, rval
    
    def show(self):
        print(self.left, self.right)

    def get(self):
        g = [self.left, self.right]
        return(g)

EMPTY_SQUARE = Card("X",0,"X",0)

class RexPlayer(object):
  """
    blueprint for player
  """

  def __init__(self):
    self.board = createBoard()
    self.startStrategy = 0 #random.randint(0,6)
    self.strategy = 0 #random.randint(0,6)

  def show(self):
    pprint.pprint(self.board)

class flop(object):
  """
  shared play space
  """

  def __init__(self, numplayers, deck):
    self.flop = []
    self.flopQueue = []
    self.selector = []

  def show(self):
      pprint.pprint(self.flop)
  def showSelect(self):
      pprint.pprint(self.selector)

def createRexDeck():
    #WHEAT = "W"
    #FOREST = "F"
    #LAKE = "L"
    #GRASS = "G"
    #SWAMP = "S"
    #MINE = "M"
    deck = [Card("W",0,"W",0),
        Card("W",0,"W",0),
        Card("F",0,"F",0),
        Card("F",0,"F",0),
        Card("F",0,"F",0),
        Card("F",0,"F",0),
        Card("L",0,"L",0),
        Card("L",0,"L",0),
        Card("L",0,"L",0),
        Card("G",0,"G",0),
        Card("G",0,"G",0),
        Card("S",0,"S",0),
        Card("W",0,"F",0),
        Card("W",0,"L",0),
        Card("W",0,"G",0),
        Card("W",0,"S",0),
        Card("F",0,"L",0),
        Card("F",0,"G",0),
        Card("W",1,"F",0),
        Card("W",1,"L",0),
        Card("W",1,"G",0),
        Card("W",1,"S",0),
        Card("W",1,"M",0),
        Card("F",1,"W",0),
        Card("F",1,"W",0),
        Card("F",1,"W",0),
        Card("F",1,"W",0),
        Card("F",1,"L",0),
        Card("F",1,"G",0),
        Card("L",1,"W",0),
        Card("L",1,"W",0),
        Card("L",1,"F",0),
        Card("L",1,"F",0),
        Card("L",1,"F",0),
        Card("L",1,"F",0),
        Card("W",0,"G",1),
        Card("L",0,"G",1),
        Card("W",0,"S",1),
        Card("G",0,"S",1),
        Card("M",1,"W",0),
        Card("W",0,"G",2),
        Card("L",0,"G",2),
        Card("W",0,"S",2),
        Card("G",0,"S",2),
        Card("M",2,"W",0),
        Card("S",0,"M",2),
        Card("S",0,"M",2),
        Card("W",0,"M",3),
        ]
    return deck

def shuffleDeck(deck):
    for i, card in enumerate(deck): # pylint: disable=unused-variable
        insert_at = random.randrange(47)
        deck[i], deck[insert_at] = deck[insert_at], deck[i]
        #deck[i].show()

def createBoard():
    board = []
    for y in range(BOARD_HEIGHT):
        board.append([])
        for x in range(BOARD_WIDTH): # pylint: disable=unused-variable
            board[y] += [EMPTY_SQUARE.left]
    # pprint.pprint(board)
    return board

def createPlayers(numplayers, players):
    for p in range(numplayers):
        print("player {}".format(p+1))
        n = RexPlayer()
        players.append(n)
        startStrategy(players, p)
        # pprint.pprint(players[p].board)


def startStrategy(player, p):
    if player[p].startStrategy is 0:
        # set castle at 4,4 center of game board
        player[p].board[(MIDDLE - 1)][(MIDDLE - 1)] = ["K", 1]

def turnStrategy(strategy, player, n, f):
    if strategy is 0:
        strategy0(player, n, f)

def strategy0(player, n, f):
    print("strategy0")
    f.selector += str(n)

def newFlop(n, d, f):
    if not f.flopQueue:
        # if flop queue empty populate flop
        for i in range(n): # pylint: disable=unused-variable
            f.flop += d[len(d)-1].get()
            d.pop()
        for i in range(n): # pylint: disable=unused-variable
        # now load flopQueue
            f.flopQueue += d[len(d)-1].get()
            d.pop()
        f.show()
    else:
        f.flop = f.flopQueue
        f.flopQueue = []
        for i in range(n): # pylint: disable=unused-variable
            f.flopQueue += d[len(d)-1].get()
            d.pop()
        f.show()

def playRound(player, n, deck, f):
    newFlop(n, deck, f)
    for p in range(n):
        turnStrategy(player[p].strategy, player[p], p, f)

def finalize(player, deck, f):
    print("finalized")

def controller(numplayers, deck):
    players = []
    f = flop(numplayers, deck)
    #f.show()
    createPlayers(numplayers, players)
    #print(len(deck))
    # while len(deck) > 0:
    #    playRound(players, numplayers, deck, f)
    playRound(players, numplayers, deck, f)
    finalize(players, deck, f)
    #print(deck[len(deck)-1].get())
    f.showSelect()

def main():
    logging.info("- Rex Brickapy!")
    deck = createRexDeck()
    shuffleDeck(deck)
    numplayers = 4 #input("Number of Players (2-6)")
    numplayers = int(numplayers)
    controller(numplayers,deck)

if __name__ == "__main__":
    main()