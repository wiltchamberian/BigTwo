# test

from test import *
from read_log import * 

if __name__ == "__main__":

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

  npc = NewNPC()

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

  pass