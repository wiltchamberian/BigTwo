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

def test3():
  al = Algorithm()

  myPlayerNum = 1
  playerlist = []
  for i in range(4):
    player = Player()
    player.handSize = 13
    playerlist.append(player)
  playerlist[0].handSize = 8
  
  myHand = ['AD', '6C', 'JD', '8S', '3H', '3D', 'KH', 'JC', '9S', '7C', '5H', 'QC', '6H']
  toBeat = Trick(3, ['7D', '8H', '9H', 'TD', 'JS'])
  matchHistory = []

  history1 = GameHistory()
  history1.winnerPlayerNum = -1
  history1.finished = False
  history1.gameHistory = []
  round = []
  trick1 = Trick(0, ['7D', '8H', '9H', 'TD', 'JS'])
  round.append(trick1)
  history1.gameHistory.append(round)

  matchHistory.append(history1)
  myData = ""
  state = MatchState(myPlayerNum,playerlist,myHand,toBeat, matchHistory, myData)
  cards, data = al.getAction(state)

  return cards, data


def test4():
  input = [ '4C','5H', '6C','7D', '8C', '8H', 'TH','QC', 'QH','KH','AC','AS','2C']
  al = Algorithm()
  handCards = transform_in(input)
  npc = NewNPC()
  box = npc.cal_good_composites(handCards)
  output =transform_box_number_to_box_character(box)
  
  print(box)
  print(output)

def test5():
  input = ['8D', '6S', 'JH', 'TS',  'KS', '9S', 'TD', '5S' , '8H']
  al = Algorithm()
  handCards = transform_in(input)

  npc = NewNPC()
  box = npc.cal_good_composites(handCards)
  output =transform_box_number_to_box_character(box)
  
  print(box)
  print(output)

def test6():
  input = ['9H', 'JD', 'QD', 'KC', '9D', '8D', '9S', 'KS', '7D', 'JS', '5S', '3D', 'TS']
  al = Algorithm()
  handCards = transform_in(input)

  npc = NewNPC()
  box = npc.cal_good_composites(handCards)
  output =transform_box_number_to_box_character(box)
  
  print(box)
  print(output)

def npc_test(input):
  al = Algorithm()
  handCards = transform_in(input)

  npc = NewNPC()
  box = npc.cal_good_composites(handCards)
  output =transform_box_number_to_box_character(box)
  
  print(box)
  print(output)
  return output