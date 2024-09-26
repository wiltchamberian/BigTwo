# test
import time
from test import *
from read_log import * 


def init_players(handSize):
  players = [Player()] * 4
  for i in range(4):
    players[i].handSize = handSize[i]
  return players

def play_card(hands, toBeat, otherHands, id, handSize, toBeatId = -1, folder_time = 0):
  startTime = time.perf_counter()

  npc = NewNPC()
  npc.current_folder_time = folder_time
  players =[Player(),Player(),Player(),Player()]
  for i in range(len(handSize)):
    players[i].handSize = handSize[i]
  leftOvers = npc.cal_otherHands_numbers(id,players)

  # box = npc.cal_good_composites(transform_in(hands), transform_in(otherHands), leftOvers)
  # with open("show_box_expectation.txt", "w") as file:
  #   for i in range(min(len(box), BOX_USE_LENGTH)):
  #     ls = []
  #     for move in box[i][0]:
  #       ls.append(transform_out(move))
  #     file.write(f"exp:{box[i][1]:.3f},len:{len(ls)}\n{ls}\n\n")

  playInfo = PlayInfo()
  playInfo.first_round_first_play = False
  playInfo.leftOvers = leftOvers
  playInfo.myHandCards = transform_in(hands)
  playInfo.otherHands = transform_in(otherHands)
  playInfo.toBeat = transform_in(toBeat)
  playInfo.toBeatId = toBeatId
  playInfo.simulate = False
  playInfo.myPlayerNum = id
  
  card, data = npc.play_card(playInfo)

  endTime = time.perf_counter()
  print(f"totalTime:{endTime-startTime:.6f}\n")

  return card,data

if __name__ == "__main__":

  for i in range(-1):
    print("abcd")

  myPlayerNum = 0
  toBeatId = 1
  myHands = ['4S', '5S', '6D', '6C', '7C', '7H', '8D', '8C', '9H', 'TD', 'QD']
  myHandsColor = []
  toBeat = ['6H', '6S']
  otherHands = ['5D', '5C', '8H', '9C', 'TH']
  handSize = [11, 1, 3, 1]
  folder_time = 0
  cards, data = play_card(myHands,toBeat,otherHands,myPlayerNum,handSize, toBeatId = toBeatId ,folder_time = folder_time) 
  assert(cards == ['7C','7H'])


  myPlayerNum = 2
  toBeatId = 3
  myHands = ['5C', '5H', '5S', '8C', 'TH', 'JC']
  myHandsColor = []
  toBeat = []
  otherHands = ['4D', '4C', '4H', '6D', '6C', '6S', '7D', '7C', '7H', '7S', '8D', '9D', '9C', 'TD', 'TC', 'TS', 'JD', 'JS', 'QD', 'KH', 'KS', '2D']
  handSize = [12, 3, 6, 7]
  folder_time = 0
  cards, data = play_card(myHands,toBeat,otherHands,myPlayerNum,handSize, toBeatId = toBeatId ,folder_time = folder_time) 

  myPlayerNum = 1
  toBeatId = -1
  myHands = ['3D', '4D', '4H', '5C', '6C', '8D', '9H', 'TD', 'TS', 'JD', '2D', '2H', '2S']
  myHandsColor = [['3D', '4D', '8D', 'TD', 'JD', '2D']]
  toBeat = []
  otherHands = ['3C', '3H', '3S', '4C', '4S', '5D', '5H', '5S', '6D', '6H', '6S', '7D', '7C', '7H', '7S', '8C', '8H', '8S', '9D', '9C', '9S', 'TC', 'TH', 'JC', 'JH', 'JS', 'QD', 'QC', 'QH', 'QS', 'KD', 'KC', 'KH', 'KS', 'AD', 'AC', 'AH', 'AS', '2C']
  handSize = [13, 13, 13, 13]
  folder_time = 0
  cards, data = play_card(myHands,toBeat,otherHands,myPlayerNum,handSize, toBeatId = toBeatId ,folder_time = folder_time) 
  assert(cards == ['3D', '4D', '8D', 'TD', 'JD'])

  myPlayerNum = 1
  toBeatId = 0
  myHands = ['9S', 'TD', 'KH', 'AS']
  myHandsColor = []
  toBeat = ['6D']
  otherHands = ['3H', '4D', '5D', '6C', '8D', 'JH', 'JS', 'KS', 'AC', '2C']
  handSize = [2, 4, 1, 7]
  folder_time = 0
  cards, data = play_card(myHands,toBeat,otherHands,myPlayerNum,handSize, toBeatId = toBeatId ,folder_time = folder_time) 
  assert(cards == ['AS'])

  myPlayerNum = 0
  toBeatId = 3
  myHands = ['3H', '6C', '7D', '9D', 'TH', 'AD', '2H', '2S']
  myHandsColor = []
  toBeat = []
  otherHands = ['4D', '4C', '4H', '4S', '5D', '5H', '6D', '7C', '7H', '7S', '8D', '8C', '8H', '8S', '9C', '9H', '9S', 'TD', 'TC', 'TS', 'JD', 'JC', 'JH', 'JS', 'QD', 'QC', 'QH', 'QS', 'KD', 'AC', 'AH', 'AS', '2D', '2C']
  handSize = [8, 13, 13, 8]
  folder_time = 0
  cards, data = play_card(myHands,toBeat,otherHands,myPlayerNum,handSize, toBeatId = toBeatId ,folder_time = folder_time) 

  myPlayerNum = 2
  toBeatId = 1
  toBeat = ['AS']
  played_cards = ['3C', '3D','5H','8S','JH','AS']
  myHands = ['2S','AH','8C', '8H', '9D', '9C', '9S','QD', 'QH', 'QS', 'KC', 'KS']
  otherHands = transform_out(complement(transform_in(myHands + played_cards)))
  handSize = [11,11,12,12]
  folder_time = 0
  cards, data = play_card(myHands,toBeat,otherHands,myPlayerNum,handSize, toBeatId = toBeatId ,folder_time = folder_time) 
  assert(cards == ['2S'])

  myPlayerNum = 2
  toBeatId = 1
  toBeat = []
  played_cards = ['3C', '3D','5H','8S','JH','AS','2S']
  myHands = ['AH','8C', '8H', '9D', '9C', '9S','QD', 'QH', 'QS', 'KC', 'KS']
  otherHands = transform_out(complement(transform_in(myHands + played_cards)))
  handSize = [11,11,11,12]
  folder_time = 0
  cards, data = play_card(myHands,toBeat,otherHands,myPlayerNum,handSize, toBeatId = toBeatId ,folder_time = folder_time) 
  assert(cards == ['8C', '8H', '9D', '9C', '9S'])


  myPlayerNum = 3
  toBeatId = 2
  myHands = ['3C', '4C', '4S', '5D', '6H', '8C', '8S', '9H', 'JS', 'KS', 'AD', 'AS', '2D']
  myHandsColor = [['4S', '8S', 'JS', 'KS', 'AS']]
  toBeat = ['7D', '7H']
  otherHands = ['3H', '4D', '4H', '6D', '8D', '8H', '9C', '9S', 'TC', 'TH', 'TS', 'JC', 'JH', 'QH', 'KC', 'KH', 'AC', 'AH', '2C', '2H', '2S']
  handSize = [6, 8, 7, 13]
  folder_time = 0
  cards, data = play_card(myHands,toBeat,otherHands,myPlayerNum,handSize, toBeatId = toBeatId ,folder_time = folder_time) 

  myPlayerNum = 3
  toBeatId = 2
  myHands = ['3C', '5D', '5S', '7C', 'TC', 'JC', 'QD', 'QC', 'QH']
  myHandsColor = [['3C', '7C', 'TC', 'JC', 'QC']]
  toBeat = []
  otherHands = ['3H', '3S', '4D', '6C', '6S', '7D', '7S', '8D', '8C', '8H', '9H', 'TD', 'KC']
  handSize = [4, 3, 6, 9]
  folder_time = 0
  cards, data = play_card(myHands,toBeat,otherHands,myPlayerNum,handSize, toBeatId = toBeatId ,folder_time = folder_time) 

  
  myPlayerNum = 1
  toBeatId = 0
  myHands = ['3S', '4C', '4H', '6D', '8D', '8C', '9C', 'KH', 'AC', 'AH', '2S']
  myHandsColor = []
  toBeat = ['QC', 'QH']
  otherHands = ['3H', '4D', '4S', '5D', '5C', '5H', '5S', '6C', '6H', '6S', '7D', '7C', '7H', '7S', '8H', '8S', '9D', '9H', '9S', 'TD', 'TC', 'TH', 'TS', 'QD', 'QS', 'KD', 'KC', 'KS', 'AD', 'AS', '2D', '2C', '2H']
  handSize = [9, 11, 13, 11]
  folder_time = 0
  cards, data = play_card(myHands,toBeat,otherHands,myPlayerNum,handSize, toBeatId = toBeatId ,folder_time = folder_time)  
  assert(cards == [])

  myPlayerNum = 1
  toBeatId = 0
  myHands = ['4D', '6C', '7H', '8C', '8H', '9H', 'QD', 'AH']
  myHandsColor = []
  toBeat = ['3H']
  otherHands = ['3S', '5D', '5C', '5H', '5S', '6D', '6H', '6S', '7D', '8D', '8S', '9D', '9C', '9S', 'TD', 'TH', 'KD', 'KC', 'KH', 'AD', 'AS', '2C', '2H']
  handSize = [8, 8, 10, 5]
  folder_time = 0
  cards, data = play_card(myHands,toBeat,otherHands,myPlayerNum,handSize, toBeatId = toBeatId ,folder_time = folder_time)  
  assert(cards == ['4D'])

  myPlayerNum = 3
  toBeatId = 2
  myHands = ['5H','6S','9D','TS','AC','AH']
  toBeat = []
  otherHands = ['4S','5D','5C','5S','6D','7D','7C','7H','7S','8D','8C','8S','9C','9H','TD','TC','JD','JC','JH','QH','QS','KD','AS','2D']
  handSize = [3,10,11,6]
  folder_time = 0
  cards, data = play_card(myHands,toBeat,otherHands,myPlayerNum,handSize, toBeatId = toBeatId ,folder_time = folder_time)  
  assert(cards == ['5H'])

  myPlayerNum = 0
  toBeatId = 1
  myHands = ['7D', '7C', '8D', 'TS', 'JD', 'JH', 'QD', 'QC', 'KS', 'AD', 'AC', '2S']
  myHandsColor = [['7D', '8D', 'JD', 'QD', 'AD']]
  toBeat = ['2C']
  otherHands = ['3H', '4D', '4C', '4H', '4S', '5D', '5H', '5S', '6D', '6C', '6H', '6S', '7H', '7S', '8C', '8H', '8S', '9C', '9S', 'TD', 'TC', 'TH', 'JC', 'JS', 'QH', 'QS', 'KH', 'AH', 'AS', '2D', '2H']
  handSize = [12, 12, 11, 8]
  folder_time = 0
  cards, data = play_card(myHands,toBeat,otherHands,myPlayerNum,handSize, toBeatId = toBeatId ,folder_time = folder_time)

  myPlayerNum = 0
  toBeatId = 3
  myHands = ['5C', '7D', '7C', '8D', 'TS', 'JD', 'JH', 'QD', 'QC', 'KS', 'AD', 'AC', '2S']
  myHandsColor = [['7D', '8D', 'JD', 'QD', 'AD']]
  toBeat = ['KD', 'KC']
  otherHands = ['3C', '3H', '4D', '4C', '4H', '4S', '5D', '5H', '5S', '6D', '6C', '6H', '6S', '7H', '7S', '8C', '8H', '8S', '9C', '9S', 'TD', 'TC', 'TH', 'JC', 'JS', 'QH', 'QS', 'KH', 'AH', 'AS', '2D', '2C', '2H']
  handSize = [13, 13, 11, 9]
  folder_time = 0
  cards, data = play_card(myHands,toBeat,otherHands,myPlayerNum,handSize, toBeatId = toBeatId ,folder_time = folder_time)

  myPlayerNum = 0
  toBeatId = 3
  myHands = ['4H', '4S', '5D', '7C', '7S', '9H', 'TH', 'JD', 'JC', 'QH', '2D']
  myHandsColor = []
  toBeat = ['6H']
  otherHands = ['3C', '3S', '4C', '5C', '5H', '6D', '6S', '7D', '7H', '8D', '8C', '8S', '9D', '9C', 'TD', 'TC', 'TS', 'JS', 'QD', 'QS', 'KD', 'KH', 'KS', 'AD', 'AH', '2H', '2S']
  handSize = [11, 9, 9, 9]
  folder_time = 0
  cards, data = play_card(myHands,toBeat,otherHands,myPlayerNum,handSize, toBeatId = toBeatId ,folder_time = folder_time)

  #exception test
  myPlayerNum = 2
  toBeatId = -1
  myHands = ['3D', '3C', '4D', '4C', '4H', '7D', '9D', '9H', '9S', 'TS', 'KH', '2D', '2S']
  myHandsColor = [['3D', '4D', '7D', '9D', '2D']]
  toBeat = []
  otherHands = ['3H', '3S', '4S', '5D', '5C', '5H', '5S', '6D', '6C', '6H', '6S', '7C', '7H', '7S', '8D', '8C', '8H', '8S', '9C', 'TD', 'TC', 'TH', 'JD', 'JC', 'JH', 'JS', 'QD', 'QC', 'QH', 'QS', 'KD', 'KC', 'KS', 'AD', 'AC', 'AH', 'AS', '2C', '2H']
  handSize = [13, 13, 13, 13]
  folder_time = 0
  cards, data = play_card(myHands,toBeat,otherHands,myPlayerNum,handSize, toBeatId = toBeatId ,folder_time = folder_time)

  myPlayerNum = 2
  toBeatId = 0
  myHands = ['5D', '6D', '6C', '6S', '9H', '9S', 'QD', 'QH', 'QS', 'AS']
  myHandsColor = []
  toBeat = []
  otherHands = ['3C', '3S', '4D', '4C', '4H', '4S', '5C', '5H', '6H', '7C', '7S', '8D', '8C', '8H', '8S', '9D', '9C', 'TD', 'TC', 'TH', 'TS', 'JD', 'JC', 'JH', 'JS', 'QC', 'KD', 'KC', 'KH', 'KS', 'AC', 'AH', '2D', '2C', '2H', '2S']
  handSize = [13, 12, 10, 11]
  folder_time = 0
  cards, data = play_card(myHands,toBeat,otherHands,myPlayerNum,handSize, toBeatId = toBeatId ,folder_time = folder_time)
  
  myPlayerNum = 2
  toBeatId = 1
  myHands = ['3C', '5D', '5C', '5H', '5S', '6D', '7H', '8H', '9D', '9C', '9H', '9S', 'TS']
  myHandsColor = []
  toBeat = ['8D', '8C', '8S']
  otherHands = ['4D', '4C', '4H', '4S', '6C', '6H', '6S', '7D', '7C', '7S', 'TD', 'TC', 'TH', 'JD', 'JC', 'JH', 'JS', 'QD', 'QC', 'QH', 'QS', 'KD', 'KC', 'KH', 'KS', 'AD', 'AC', 'AH', 'AS', '2D', '2C', '2H', '2S']
  handSize = [10, 10, 13, 13]
  folder_time = 0
  cards, data = play_card(myHands,toBeat,otherHands,myPlayerNum,handSize, toBeatId = toBeatId ,folder_time = folder_time)
 

  myPlayerNum = 1
  toBeatId = 0
  myHands = ['3H', '3S', '5S', '6D', '6C', '7C', '8H', '9H', '9S', 'QD', 'QC', 'AH', '2H']
  myHandsColor = [['3H', '8H', '9H', 'AH', '2H']]
  toBeat = ['3C'] 
  otherHands = ['4D', '4C', '4H', '4S', '5D', '5C', '5H', '6H', '6S', '7D', '7H', '7S', '8D', '8C', '8S', '9D', '9C', 'TD', 'TC', 'TH', 'TS', 'JD', 'JC', 'JH', 'JS', 'QH', 'QS', 'KD', 'KC', 'KH', 'KS', 'AD', 'AC', 'AS', '2D', '2C', '2S']
  handSize = [12, 13, 13, 12]
  folder_time = 0
  cards, data = play_card(myHands,toBeat,otherHands,myPlayerNum,handSize, toBeatId = toBeatId ,folder_time = folder_time)

  myPlayerNum = 0
  toBeatId = 1
  myHands = ['9S', 'TD', 'TS', 'JH', 'QD', '2D', '2C', '2S']
  myHandsColor = []
  toBeat = []
  otherHands = ['3H', '3S', '4D', '4C', '4H', '4S', '5D', '5C', '5H', '5S', '6D', '6C', '6H', '6S', '7H', '8D', '8C', '8H', '8S', '9D', '9C', '9H', 'TC', 'TH', 'JD', 'JC', 'JS', 'QC', 'QH', 'QS', 'KD', 'KC', 'KH', 'KS', 'AD', 'AC', 'AH', 'AS', '2H']
  handSize = [8, 13, 13, 13]
  folder_time = 0
  cards, data = play_card(myHands,toBeat,otherHands,myPlayerNum,handSize, toBeatId = toBeatId ,folder_time = folder_time)

  myPlayerNum = 0
  toBeatId = 3
  myHands = ['4D', '4S', '5D', '5S', '6H', '7C', '7H', '8C', '8S', 'QC', '2D', '2H', '2S']
  myHandsColor = []
  toBeat = ['9C', 'TS', 'JS', 'QD', 'KC']
  otherHands = ['3C', '4C', '4H', '5C', '5H', '8D', '8H', '9D', '9H', '9S', 'TD', 'TC', 'TH', 'JD', 'JC', 'JH', 'QH', 'QS', 'KD', 'KH', 'KS', 'AC', 'AH', '2C']
  handSize = [13, 13, 8, 3]
  folder_time = 0
  cards, data = play_card(myHands,toBeat,otherHands,myPlayerNum,handSize, toBeatId = toBeatId ,folder_time = folder_time)

  myPlayerNum = 0
  toBeatId = 3
  myHands = ['4C', 'KD', 'KC']
  myHandsColor = []
  toBeat = ['5H']
  otherHands = ['3H', '4D', '4H', '6C', '7S', '8D', '8H', '8S', '9D', '9H', '9S', 'TH', 'JC', 'JH', 'JS', 'QC', 'KH', 'KS', 'AD', 'AC', 'AH', '2H', '2S']
  handSize = [3, 8, 8, 7]
  folder_time = 0
  cards, data = play_card(myHands,toBeat,otherHands,myPlayerNum,handSize, toBeatId = toBeatId ,folder_time = folder_time)

  myPlayerNum = 0
  toBeatId = 3
  myHands = ['5D', '5S', '7D', '7C', '7S', '8D', '9C', '9H', 'TS', 'JC', 'KS', 'AC']
  myHandsColor = []
  toBeat = ['4D', '4C', '4H', '2H', '2S']
  otherHands = ['3C', '3S', '5C', '5H', '6D', '6C', '6H', '6S', '7H', '8C', '8H', '8S', '9D', '9S', 'TD', 'TC', 'TH', 'JD', 'JH', 'QD', 'QH', 'QS', 'KD', 'KC', 'AH', 'AS']
  handSize = [12, 12, 7, 7]
  folder_time = 0
  cards, data = play_card(myHands,toBeat,otherHands,myPlayerNum,handSize, toBeatId = toBeatId ,folder_time = folder_time)

  myPlayerNum = 1
  toBeatId = 3
  myHands = ['5C', '6S', 'TC', 'TH', 'JS', 'KS', 'AD']
  myHandsColor = []
  toBeat = []
  otherHands = ['3S', '4D', '4C', '4H', '4S', '5D', '5H', '5S', '6D', '6C', '7H', '7S', '8C', 'TD', 'TS', 'JD', 'JC', 'JH', 'QS', 'KD', 'KC', 'AC', '2C']
  handSize = [9, 7, 5, 9]
  folder_time = 0
  cards, data = play_card(myHands,toBeat,otherHands,myPlayerNum,handSize, toBeatId = toBeatId ,folder_time = folder_time)

  myPlayerNum = 1
  toBeatId = 0
  myHands = ['6D', '6C', '8D', '8C', '8S', '9D', '9C', 'TD', 'TS', 'JH', 'QS', '2H']
  myHandsColor = []
  toBeat = ['KH']
  otherHands = ['4D', '4C', '4H', '4S', '5D', '5C', '5H', '5S', '6H', '6S', '7D', '7C', '7H', '8H', '9H', 'TC', 'TH', 'JD', 'JC', 'JS', 'QH', 'KD', 'KC', 'AD', '2D', '2S']
  handSize = [10, 12, 5, 11]
  folder_time = 2
  cards, data = play_card(myHands,toBeat,otherHands,myPlayerNum,handSize, toBeatId = toBeatId ,folder_time = folder_time)
  #assert(cards == [])

  myPlayerNum = 2
  toBeatId = 1
  myHands = ['4D', '5D', '5H', '6C', '8C', '9D', 'TH', 'JC', 'JH', 'QS', 'KS', '2C']
  myHandsColor = []
  toBeat = ['AD']
  otherHands = ['3H', '4C', '5C', '6D', '7D', '7C', '7H', '8D', '8H', '9C', '9H', '9S', 'TD', 'TC', 'TS', 'JD', 'JS', 'QD', 'QC', 'QH', 'KD', 'KC', 'KH', '2D', '2S']
  handSize = [10, 11, 12, 4]
  folder_time = MAX_FOLDER_TIME_IN_A_GAME
  cards, data = play_card(myHands,toBeat,otherHands,myPlayerNum,handSize, toBeatId = toBeatId ,folder_time = folder_time)
  assert(cards == [])

  myPlayerNum = 1
  toBeatId = 0
  myHands = ['4H', '5S', '6D', '6C', '6S', '7C', '7H', '8C', '8H', '9C', 'TS', 'JD', 'KH']
  myHandsColor = []
  toBeat = ['KC']
  otherHands = ['3C', '3H', '3S', '4D', '4C', '4S', '5D', '5C', '5H', '6H', '7D', '7S', '8D', '8S', '9D', '9H', '9S', 'TD', 'TC', 'TH', 'JC', 'JH', 'JS', 'QD', 'QC', 'QH', 'QS', 'KD', 'KS', 'AD', 'AC', 'AH', 'AS', '2D', '2C', '2H', '2S']
  handSize = [12, 13, 13, 12]
  cards, data = play_card(myHands,toBeat,otherHands,myPlayerNum,handSize, toBeatId = toBeatId)

  myPlayerNum = 1
  myHands = ['9S', 'TH', 'TS', 'JC', 'JH']
  myHandsColor = []
  toBeat = []
  otherHands = ['3C', '3S', '4S', '5D', '5S', '6C', '6H', '6S', '7D', '7C', '9C', 'TD', 'TC', 'JS', 'QC', 'QH', 'KC', 'KH', 'KS', 'AC', 'AH', 'AS', '2C']
  handSize = [6, 5, 11, 6]
  cards, data = play_card(myHands,toBeat,otherHands,myPlayerNum,handSize)
  assert(cards == ['TH','TS'])

  myPlayerNum = 1
  myHands = ['3D', '6D', '7H', '9S', 'TH', 'TS', 'JC', 'JH', 'QD', 'QS', 'AD', '2D', '2S']
  myHandsColor = [['3D', '6D', 'QD', 'AD', '2D']]
  toBeat = []
  otherHands = ['3C', '3H', '3S', '4D', '4C', '4H', '4S', '5D', '5C', '5H', '5S', '6C', '6H', '6S', '7D', '7C', '7S', '8D', '8C', '8H', '8S', '9D', '9C', '9H', 'TD', 'TC', 'JD', 'JS', 'QC', 'QH', 'KD', 'KC', 'KH', 'KS', 'AC', 'AH', 'AS', '2C', '2H']
  handSize = [13, 13, 13, 13]

  cards, data = play_card(myHands,toBeat,otherHands,myPlayerNum,handSize)


  cards, data = play_card(['4C', '4S', '6D', '6H', '8C', 'JH'], [],['3C', '3H', '4H', '5H', '5S', '6C', '8H', 'QS', 'KC', 'KH'],0 ,[6, 1, 6, 3])
  assert(cards == ['4C', '4S'])
  
  cards, data = play_card(['3C', '4D', '5D', '5C', '7H', '8H', '9S', 'QD', 'QC', 'QS', 'KS'],[],['4H', '5H', '5S', '7D', '7C', '7S', '8D', '8C', '8S', '9D', '9C', '9H', 'JC', 'QH'],1,[6, 11, 1, 7] )
  #assert (cards == ['5D','5C','QD','QC','QS'])

  cards, data = play_card(['4H', 'TC'],[],['3C', '3H', '4D', '4C', '5H', '6D', '6H', '7H', '8D', '8H', '8S', '9D', 'TD', 'TH', 'TS', 'JD', 'JS', 'KD', 'KC', 'KH', 'KS', 'AD', '2D', '2C'], 0, [2, 6, 12, 6] )
  assert (cards== ['4H'])

  cards, data = play_card( ['6H', '9S', 'TC', 'TS', 'QH', '2D', '2C', '2S'],[], ['3H', '3S', '4D', '5H', '5S', '6D', '6C', '6S', '7D', '7H', '7S', '8D', '8C', '8S', '9H', 'TD', 'TH', 'JC', 'JS', 'KC', 'KH', 'KS', 'AD', 'AC'],0,[8,8,8,8])
  assert (cards ==['6H'])

  cards, data = play_card( ['5H', '7D', 'TC', 'TS', 'QC', 'KD', '2H', '2S'],[], ['3S', '4H', '5C', '5S', '7C', '7H', '7S', '8D', '8C', '8H', '8S', '9D', 'TD', 'TH', 'JD', 'JC', 'JH', 'QD', 'QH', 'QS', 'KH', 'AD', 'AC', 'AS'],0,[8,8,8,8])
  assert (cards ==['5H'])
  
  cards, data = play_card(['5C', '6D', '6C', '6S', '7D', '9C', 'QD', '2S'],[], ['3D', '4D', '4H', '5D', '5H', '6H', '7C', '8D', '8H', '9D', '9H', '9S', 'TD', 'TC', 'TS', 'JD', 'JS', 'QC', 'KC', 'KH', 'AC', 'AH', 'AS', '2H'],0,[8,8,8,8])
  assert (cards==['5C'])

 
  
  pass