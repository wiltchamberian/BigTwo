# test

from test import *
from read_log import * 

if __name__ == "__main__":
  npc = NewNPC()

  s12 = ['3C', '3S', '4H', '5H', '6D', '6S', '7H', '9S', 'TD', 'TH', 'JS', 'QS', '2D']
  toBeat12 =['7S']
  otherHands12 = ['4C', '5D', '6C', '6H', '7D', '7C', '8D', '8C', '8H', '8S', '9D', '9C', '9H', 'JH', 'QD', 'QC', 'QH', 'KD', 'KH', 'AD', 'AC', 'AH', 'AS', '2S']
  card12,data = npc.play_card(transform_in(s12), transform_in(otherHands12), transform_in(toBeat12), 0, simulate = False)

  s11 = ['4H', '5H', '7C', '7H', '7S', 'TD', 'JS', 'QS', 'AS', '2H', '2S']
  other11 = ['KC', 'KS']
  card11,data = npc.play_card(transform_in(s11), None, transform_in(other11), 0, simulate = False)

  s10 = ['4C', '5H', '6D', '6C', '6S', '8C', 'TD', 'QD', 'QS', 'KH', 'AD', 'AC', '2H']
  other10 = ['3C']
  card10, data = npc.play_card(transform_in(s10), None, transform_in(other10), 0, simulate = False)

  s9 = ['3S', '4C', '4S', '5C', 'TS', 'JH', 'JS', 'QS']
  other9 = []
  card9, data = npc.play_card(transform_in(s9), None, transform_in(other9), 0, simulate = True)

  pass
  # gamePlays = read_log("C:\\Users\\dell\\Downloads\\logfile25385.txt")
  # write_log(gamePlays)
  # print("write_done!\n")
  # cards, data = test3()

  # test4()

  #test3()

  card1 = [10,1]
  card2 = [4,5,6]
  strategy = [card2,card1]
  #strategy = sort_strategy(strategy)

  
  s01 =['4D', 'TH', '3H', 'AH', 'AD', '8C', '7C', '3S', 'TS', '7S', '3C', '3D', '5C']
  npc.play_card(transform_in(s01),None,transform_in([]),0, simulate = True)

  s0 = ['3H','4H','5H','6H','7H','4D','5D','6D','7S','8C','AS','AH','2D']
  card0,data = npc.play_card(transform_in(s0),None,transform_in([]),0)

  s1 = ['5D','6C','6H','9D','TC','TH','JS','QD','KH','KS','AH','2C']
  output1 = npc_test(s1)
  cards1, data = npc.play_card(transform_in(s1), None, [], 0, simulate = True)

  s2 = ['3H','6C','9C','9S','KH','AD']
  output2 = npc_test(s2)
  cards2, data = npc.play_card(transform_in(s2), None, [], 0, simulate = True)

  s3 = ['6D',  'QD', 'AD', 'QS', 'KD', 'KH',  '4H', '4C', '6S', 'AH']
  other3 = ['9S']
  card3,data = npc.play_card(transform_in(s3),None,transform_in(other3),0, simulate = True)

  s4 =['2D', '4C', 'KD', '8C', '5H', '5D', 'TD', '3H', '8H', 'JS', '7H', '5C', 'AS']
  other4 = ['6S', '6H', '6C', '6D', 'AC']
  card4, data = npc.play_card(transform_in(s4), None, transform_in(other4), 0, simulate = True)

  s5 = ['3H', '7C', '3S', '4C', '3C', '8S', '9H', 'AS', 'QS', '7H', '2D', 'KH', '7S']
  other5 = ['6D', '6C', '6S', 'QD', 'QH']
  card5, data = npc.play_card(transform_in(s5), None, transform_in(other5), 0, simulate = True)
  
  s6 = ['3C', '3S', '4C', '4H', '8D', '8C', '8H', '9C', 'AC']
  other6 = ['7S']
  card6, data = npc.play_card(transform_in(s6), None, transform_in(other6), 0, simulate = True)

  s7 = ['5C', '7D', '7H', '8C', 'TC', 'JD', 'JC', 'QC', 'QH', 'AD', 'AC']
  other7 = ['KS']
  card7, data = npc.play_card(transform_in(s7), None, transform_in(other7), 0, simulate = True)

  s8 = ['3C', '4C', '4S', '5C', '6D', '7D', '8C', '9C', 'QC', 'KD', 'KS']
  other8 = ['6C']
  card8, data = npc.play_card(transform_in(s8), None, transform_in(other8), 0, simulate = True)

 
  
  pass