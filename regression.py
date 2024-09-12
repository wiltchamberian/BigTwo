from game import *
from helper import *


def regression_test():
  game = GameManager()
  npc = game.create_simulator()
  output = npc.cal_5card_possible_moves((0,1,2,3,4),1)
  print(f"all_straight:{len(npc.all_straight)}\n")
  print(f"all_flush:{len(npc.all_flush)}\n")
  print(f"all_four_of_a_kind:{len(npc.all_four_of_a_kind)}\n")
  print(f"all_full_house:{len(npc.all_full_house)}\n")
  print(f"all_straight_flush:{len(npc.all_straight_flush)}\n")
  sum = len(npc.all_straight) + len(npc.all_flush) + len(npc.all_four_of_a_kind)
  + len(npc.all_full_house) + len(npc.all_straight_flush)
  print(f"sum:{sum}\n")

  game = GameManager()
  cards = create_shuffled_cards()

  npc0 = game.create_simulator()
  for i in range(0,13):
    npc0.card_state[cards[i]] = IN_MY_HAND

  npc1 = game.create_simulator()
  for i in range(13,26):
    npc1.card_state[cards[i]] = IN_MY_HAND

  npc2 = game.create_simulator()
  for i in range(0,13):
    pass

  print(f"my_cards:\n")
  

  print("good!")