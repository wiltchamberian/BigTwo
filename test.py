from algorithm import *


def test1():
  al = Algorithm()

  myPlayerNum = 2
  playerlist = []
  for i in range(4):
    player = Player()
    player.handSize = 13
    playerlist.append(player)
  playerlist[3].handSize = 11
  playerlist[1].handSize = 11
  
  myHand = ['3D','3H','5H','6C','6S','8S','9D','TD','JC','KC','AD','AH','2S']

  toBeat = Trick(1, ['4D','4C'])
  matchHistory = []
  history0 = GameHistory()
  history0.finished = True

  history1 = GameHistory()
  history1.winnerPlayerNum = -1
  history1.finished = False
  history1.gameHistory = []
  round = []
  trick1 = Trick(3, ['3S', '3C'])
  trick2 = Trick(0, [])
  trick3 = Trick(1, ['4D','4C'])
  round.append(trick1)
  round.append(trick2)
  round.append(trick3)
  history1.gameHistory.append(round)


  matchHistory.append(history0)
  matchHistory.append(history1)
  myData = ""
  state = MatchState(myPlayerNum,playerlist,myHand,toBeat, matchHistory, myData)
  cards, data = al.getAction(state)

  return cards, data



def test2():
  al = Algorithm()

  myPlayerNum = 2
  playerlist = []
  for i in range(4):
    player = Player()
    player.handSize = 13
    playerlist.append(player)
  playerlist[3].handSize = 8
  
  myHand = ['3C','3H','5H','6C','6S','6D','6H','TD','JC','KC','AD','AH','2S']

  toBeat = Trick(3, ['4D','4C','4S','4H','3D'])
  matchHistory = []
  history0 = GameHistory()
  history0.finished = True

  history1 = GameHistory()
  history1.winnerPlayerNum = -1
  history1.finished = False
  history1.gameHistory = []
  round = []
  trick1 = Trick(3, ['4D','4C','4S','4H','3D'])
  trick2 = Trick(0, [])
  trick3 = Trick(1, [])
  round.append(trick1)
  round.append(trick2)
  round.append(trick3)
  history1.gameHistory.append(round)


  matchHistory.append(history0)
  matchHistory.append(history1)
  myData = ""
  state = MatchState(myPlayerNum,playerlist,myHand,toBeat, matchHistory, myData)
  cards, data = al.getAction(state)

  return cards, data