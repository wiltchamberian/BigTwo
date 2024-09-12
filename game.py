from npc import *
import copy



#GameManger is also the player
class GameManager:
  def __init__(self):
    #these are states, be careful!
    self.state = [IN_OTHER_HAND] * 52
    self.p1_num_card = 13
    self.p2_num_card = 13
    self.p3_num_card = 13



    self.all_straight, self.all_straight_flush = find_all_straight_and_straight_flush()
    self.all_four_of_a_kind = find_all_four_of_a_kind()
    self.all_full_house = find_all_full_house()
    self.all_flush = find_all_flush()

  def create_simulator(self):
    npc = NPC()
    npc.card_state = copy.deepcopy(self.state)
    npc.all_straight = self.all_straight
    npc.all_straight_flush = self.all_straight_flush
    npc.all_four_of_a_kind = self.all_four_of_a_kind
    npc.all_full_house = self.all_full_house
    npc.all_flush = self.all_flush
    return npc

  def to_played(self,cards):
    for card in cards:
      self.state[card] = CARD_PLAYED

  #interface for system
  def run(self, p1_cards, p2_cards, p3_cards):
    self.to_played(p1_cards)
    self.p1_num_card -= len(p1_cards)
    self.to_played(p2_cards)
    self.p2_num_card -= len(p2_cards)
    self.to_played(p3_cards)
    self.p3_num_card -= len(p3_cards)
    
    playing_cards = []
    if len(p3_cards)!=0 :
      playing_cards = self.follow_play(p3_cards)
    elif len(p2_cards)!=0:
      playing_cards = self.follow_play(p2_cards)
    elif len(p1_cards)!=0:
      playing_cards = self.follow_play(p1_cards)
    else:
      playing_cards = self.play()

    self.see(playing_cards)
    return playing_cards

    
  def see(self,cards):
    for card in cards:
      self.state[card] = CARD_PLAYED
    return

  def play(self):
    return self.follow_play([])

  def follow_play(self, cards):
    npc0 = self.create_simulator()
    output = npc0.cal_possible_moves(cards)
    if output == None or len(output) == 0:
      return []

    # for possible output simulate
    max_nums = 20
    max_value = 0
    result = []
    for cards in output:
      total_value = 0
      for i in range(10):
        value = self.simulate1(cards)
        total_value += value 
      if(max_value < total_value):
        max_value = total_value
        result  = cards

    self.to_played(result)
    return result

    
  def simulate1(self, cards):
    #从没有出的牌里随机分配一些,制造3个npc 

    #制造一个npc 模拟自己
    npc0 = self.create_simulator()
    #制造一个大npc 模拟敌人
    npc = self.create_simulator()
    for i in 52:
      if self.state[i] == IN_MY_HAND:
        npc.card_state[i] = IN_OTHER_HAND
      elif self.state[i] == CARD_PLAYED:
        npc.card_state[i] = CARD_PLAYED
      elif self.state[i] == IN_OTHER_HAND:
        npc.card_state[i] = IN_MY_HAND 
    for card in cards:
      npc.card_state[card] = CARD_PLAYED
    
    who_wins = 0
    total_play_num = 0
    for i in range(10):
      npc.see(cards)
      output = npc.cal_possible_moves(cards)
      if(len(output) == 0):
        who_wins = 0
        break
      r_index = random.randint(0, len(output))
      new_cards = output[r_index]
      npc.play(new_cards)
      total_play_num += 1

      npc0.see(new_cards)
      output0 = npc0.cal_possible_moves(new_cards)
      if(len(output0) == 0):
        who_wins = 1
        break
      r_index0 = random.randint(0, len(output0))
      cards = output0[r_index0]
      npc0.see(cards)
      total_play_num += 1

    if who_wins == 0:
      return 20
    else:
      return total_play_num
