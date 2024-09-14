#Monte Carlo tree search
import random
import copy

from helper import * 
class NPC:
  def __init__(self, state, table:Table):
    self.card_state = state
    if table != None:
      self.all_straight = table.all_straight
      self.all_straight_flush = table.all_four_of_a_kind
      self.all_flush = table.all_flush
      self.all_four_of_a_kind = table.all_four_of_a_kind
      self.all_full_house = table.all_full_house

  def build(self, handCards):
    self.card_state = [CARD_PLAYED] * 52
    for card in handCards:
      self.card_state[card] = IN_MY_HAND 
    return

  #interface
  def see(self, cards):
    for card in cards:
      self.card_state[card] = CARD_PLAYED

  def play(self, cards):
    if self.is_legal_play(cards):
      for card in cards:
        self.card_state[card] = CARD_PLAYED
    else:
      return False

  #cards are seen as set, so the order may be changed
  def is_legal_play(self, cards):
    l = len(cards)
    if l!=1 or l!=2 or l!=3 or l!=5:
      return False
    
    if l == 1:
      if self.card_state[cards[0]] == IN_MY_HAND:
        return True 
      else:
        return False
    elif l == 2:
      if get_rank(cards[0]) != get_rank(cards[1]):
        return False
      else:
        if self.card_state[cards[0]] == IN_MY_HAND and self.card_state[cards[1]] == IN_MY_HAND:
          return True
        else:
          return False
    elif l == 3:
      if (get_rank(cards[0]) != get_rank(cards[1])) or (get_rank(cards[0])!=get_rank(cards[2])):
        return False
      else:
        if self.card_state[cards[0]] == IN_MY_HAND and self.card_state[cards[1]] == IN_MY_HAND  and self.card_state[cards[2]] == IN_MY_HAND:
          return True 
        else:
          return False
    elif l == 5:
      tp = card5_type(cards)
      if tp == NOTHING:
        return False 
      return True
    else:
      return False

  def cal_one_card_moves(self, cards):
    output = []
    if cards == None or len(cards) == 0:
      for i in range(0, 52):
        if self.card_state[i] == IN_MY_HAND:
          output.append((i))
    else:
      card = cards[0]
      for i in range(card + 1,52):
        if self.card_state[i] == IN_MY_HAND:
          output.append((i))
    return output
  
  def cal_two_cards_moves(self, cards):
    output = []
    max_card = 1
    if cards == None or len(cards) == 0:
      max_card = 1
    else:
      max_card = max(cards[0],cards[1])
    for i in range(max_card + 1,52):
        if self.card_state[i] == IN_MY_HAND:
          for j in range(i - 1,i-(i%4)-1, -1):   
            if self.card_state[j] == IN_MY_HAND:
              output.append((i,j))
    return output
      
  def cal_three_cards_moves(self, cards):
    output = []
    if cards == None or len(cards)==0 :
      rank = 0
      l = 3
    else:
      rank = self.get_rank(cards[0])
      l = rank+4 - (rank%4) +3
    for i in range(l, 52, 4):
      if(self.card_state[i-3]==IN_MY_HAND
          and self.card_state[i-2]==IN_MY_HAND
          and self.card_state[i-1]==IN_MY_HAND):
        output.append((i-1,i-2,i-3))
      if(self.card_state[i] == IN_MY_HAND
          and self.card_state[i-3]==IN_MY_HAND
          and self.card_state[i-2] == IN_MY_HAND):
        output.append((i, i-2,i-3))
      if(self.card_state[i] == IN_MY_HAND
          and self.card_state[i-3] == IN_MY_HAND
          and self.card_state[i-1] == IN_MY_HAND):
        output.append((i,i-3,i-1))
      if(self.card_state[i] == IN_MY_HAND
          and self.card_state[i-1] == IN_MY_HAND
          and self.card_state[i-2] == IN_MY_HAND):
        output.append((i,i-1,i-2))
    return output
  
  def contain(self, cards, flag):
    return self.card_state[cards[0]] == flag and self.card_state[cards[1]] == flag and self.card_state[cards[2]]==flag and self.card_state[cards[3]]==flag and self.card_state[cards[4]]==flag

  def pick_all_contains(self, composites, index, flag):
    output = []
    for i in range(index, len(composites)):
      if(self.contain(composites[i],flag)):
        output.append(composites[i])  
    return output

  def cal_straight_new(self, handGroup, cards):
    output = []
    for i in range(0, len(handGroup)-4):
      bingo = True
      for j in range(i+1, i+5):
        if get_rank(handGroup[j][0]) != (get_rank(handGroup[j-1][0])+1):
          bingo = False
          break
      if bingo:
        for c1 in handGroup[i]:
          for c2 in handGroup[i+1]:
            for c3 in handGroup[i+2]:
              for c4 in handGroup[i+3]:
                for c5 in handGroup[i+4]:
                  playCards = [c1,c2,c3,c4,c5]
                  if (cards == None or len(cards) == 0):
                    output.append(playCards)
                  else:
                    res = compare5_straight(playCards, cards)
                    if(res == GREATER):
                      output.append(playCards)
    return output     

  def cal_flush_new(self, flushGroup, cards):
    output = []
    for i in range(0,len(flushGroup)):
      if len(flushGroup[i])<5:
          continue
      
      if cards == None or len(cards) == 0:
        return [flushGroup[i][0:5]]
      
      for j in range(4, len(flushGroup[i])):
        if flushGroup[i][j] > cards[-1]:
          return [flushGroup[i][j:j+5]]

    return output

  def cal_full_house_new(self, handGroup, cards):
    output = [] 
    for i in range(len(handGroup)):
      if len(handGroup[i]) ==3 :
        for j in range(len(handGroup)):
          if j!=i and len(handGroup[j]) ==2:
            tmp = sorted(handGroup[i]+handGroup[j])
            if cards == None or len(cards) == 0:
              output.append(tmp)
            else:
              if compare5_full_house(tmp, cards) == GREATER:
                output.append(tmp)
              
  
  def cal_four_in_a_kind_new(self, handGroup, cards):
    output = [] 
    for i in range(len(handGroup)):
      if len(handGroup[i]) == 4 :
        for j in range(len(handGroup)):
          if j!=i and len(handGroup[j]) ==1:
            tmp = sorted(handGroup[i]+handGroup[j])
            if cards == None or len(cards) == 0:
              output.append(tmp)
              return output
            else:
              if compare5_four_of_a_kind(tmp, cards) == GREATER:
                output.append(tmp)
                return output
    return output
  
  def cal_straight_flush_new(self, flushGroup, cards):
    output = []
    for flush in flushGroup:
      for i in range(len(flush) - 4):
        bingo = True
        for j in range(i+1, i+5):
          if flush[j] != flush[j-1] + 4:
            bingo = False
        if bingo:
          tmp = flush[i:i+5]
          if cards == None or len(cards) == 0:
            output.append(tmp)
          else:
            if compare5_straight_flush(tmp, cards) == GREATER:
              output.append(tmp)
    return output


  def cal_5card_possible_moves_new(self, cards):
    myHandGroup = [] #group according to rank
    myFlushGroup = [] #group according to suit

    group = []
    for i in range(len(self.card_state)):
      if self.card_state[i] == IN_MY_HAND:
        rank = get_rank(i)
        if len(group) == 0:
          group.append(i)
        else:
          if rank == get_rank(group[0]):
            group.append(i)
          else:
            myHandGroup.append(copy.deepcopy(group))
            group = [i]

    group0 = []
    group1 = []
    group2 = []
    group3 = []
    for i in range(0, len(self.card_state), 4):
      if self.card_state[i] == IN_MY_HAND:
        group0.append(i)
    for i in range(1, len(self.card_state), 4):
      if self.card_state[i] == IN_MY_HAND:
        group1.append(i)
    for i in range(2, len(self.card_state), 4):
      if self.card_state[i] == IN_MY_HAND:
        group2.append(i)
    for i in range(3, len(self.card_state), 4):
      if self.card_state[i] == IN_MY_HAND:
        group3.append(i)  
    myFlushGroup.append(group0)
    myFlushGroup.append(group1)
    myFlushGroup.append(group2)
    myFlushGroup.append(group3)
    
    output = []
    if cards == None or len(cards) == 0:
      output += self.cal_straight_new(myHandGroup, cards)
      output += self.cal_flush_new(myFlushGroup, cards)
      output += self.cal_full_house_new(myHandGroup, cards)
      output += self.cal_four_in_a_kind_new(myHandGroup, cards)
      output += self.cal_straight_flush_new(myFlushGroup, cards)
      return output
     
    cards = sorted(cards)
    type = card5_type(cards)
    if type == STRAIGHT:
      output += self.cal_straight_new(myHandGroup, cards)
      output += self.cal_flush_new(myFlushGroup, cards)
      output += self.cal_full_house_new(myHandGroup, cards)
      output += self.cal_four_in_a_kind_new(myHandGroup, cards)
      output += self.cal_straight_flush_new(myFlushGroup, cards)
    elif type == FLUSH:
      output += self.cal_flush_new(myFlushGroup, cards)
      output += self.cal_full_house_new(myHandGroup, cards)
      output += self.cal_four_in_a_kind_new(myHandGroup, cards)
      output += self.cal_straight_flush_new(myFlushGroup, cards)
    elif type == FULL_HOUSE:
      output += self.cal_full_house_new(myHandGroup, cards)
      output += self.cal_four_in_a_kind_new(myHandGroup, cards)
      output += self.cal_straight_flush_new(myFlushGroup, cards)
    elif type == FOUR_OF_A_KIND:
      output += self.cal_four_in_a_kind_new(myHandGroup, cards)
      output += self.cal_straight_flush_new(myFlushGroup, cards)
    elif type == STRAIGHT_FLUSH:
      output += self.cal_straight_flush_new(myFlushGroup, cards)

    return output
  
  def cal_5card_possible_moves(self, cards):
    flag = IN_MY_HAND
    if cards == None or len(cards) == 0:
      output = []
      output += self.pick_all_contains(self.all_straight, 0, flag)
      output += self.pick_all_contains(self.all_flush, 0, flag)
      output += self.pick_all_contains(self.all_four_of_a_kind, 0, flag)
      output += self.pick_all_contains(self.all_full_house, 0, flag)
      output += self.pick_all_contains(self.all_straight_flush, 0, flag)
      return output

    cards = sorted(cards)
    type = card5_type(cards)
    output = []
    
    if type == STRAIGHT:
      index = binary_search(self.all_straight,cards, compare5_straight)
      output += self.pick_all_contains(self.all_straight, index + 1, flag)
      output += self.pick_all_contains(self.all_flush, 0, flag)
      output += self.pick_all_contains(self.all_four_of_a_kind, 0, flag)
      output += self.pick_all_contains(self.all_full_house, 0, flag)
      output += self.pick_all_contains(self.all_straight_flush, 0, flag)
      return output
    elif type == FLUSH:
      index = binary_search(self.all_flush,cards, compare5_flush)
      output += self.pick_all_contains(self.all_flush,index+1,flag)
      output += self.pick_all_contains(self.all_four_of_a_kind, 0, flag)
      output += self.pick_all_contains(self.all_full_house, 0, flag)
      output += self.pick_all_contains(self.all_straight_flush, 0 , flag)
      return output
    elif type == FULL_HOUSE:
      index = binary_search(self.all_full_house,cards, compare5_full_house)
      output += self.pick_all_contains(self.all_full_house, index + 1, flag)
      output += self.pick_all_contains(self.all_four_of_a_kind, 0, flag)
      output += self.pick_all_contains(self.all_straight_flush, 0 , flag)
      return output     
    elif type == FOUR_OF_A_KIND:
      index = binary_search(self.all_four_of_a_kind,cards, compare5_four_of_a_kind)
      output += self.pick_all_contains(self.all_four_of_a_kind, index + 1, flag)
      output += self.pick_all_contains(self.all_straight_flush, 0 , flag)
      return output
    elif type == STRAIGHT_FLUSH:
      index = binary_search(self.all_straight_flush,cards, compare5_straight_flush)
      output += self.pick_all_contains(self.all_straight_flush, index+1 , flag)
      return output  

    return output

  def cal_possible_moves(self, cards):
    output = []
    if  cards == None or len(cards) == 0:
      output = output + self.cal_one_card_moves(None)
      output = output + self.cal_two_cards_moves(None)
      output = output + self.cal_three_cards_moves(None)
      output = output + self.cal_5card_possible_moves_new(None)
    elif len(cards) == 1:
      return self.cal_one_card_moves(cards)
    elif len(cards) == 2:
      return self.cal_two_cards_moves(cards)
    elif len(cards) == 3:
      return self.cal_three_cards_moves(cards)
    elif len(cards) == 5:
      return self.cal_5card_possible_moves_new(cards)
    return output
  
  def play_random(self, cards):
    moves = self.cal_possible_moves(cards)
    if moves == None or len(moves) == 0:
      return None
    number = random.randint(0, len(moves)-1)
    self.see(moves[number])
    return moves[number]
  
  #generate a legal random play, but not actually play
  def legal_random(self, cards):
    moves = self.cal_possible_moves(cards)
    if moves == None or len(moves) == 0:
      return None
    number = random.randint(0, len(moves)-1)
    return moves[number]   

  