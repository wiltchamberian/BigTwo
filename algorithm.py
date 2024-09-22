from classes import *

VERSION = "2.18.6_expectation_update_fix_bug"

import copy
from functools import cmp_to_key
#####################helper#########################
import random 
import time


STRATEGY_TYPE_LEN = 0
STRATEGY_TYPE_PROBABILITY = 1
STRATEGY_TYPE_EXPECTATION = 2


#choose strategy
STRATEGY_TYPE = STRATEGY_TYPE_EXPECTATION
MAX_FOLDER_TIME_IN_A_GAME = 2
MIN_NUM_CARD_IN_OTHER_HAND_FOR_FOLDER = 3




#play_type
FOLDER = 0
NOBEAT = 1
PLAY_CARD = 2



BOX_USE_LENGTH = 20

CARD_3D = 0

IN_MY_HAND = 0
IN_OTHER_HAND = 1
CARD_PLAYED = 2

#self is always number 0 player
FOLLOW0 = 0
FOLLOW1 = 1
FOLLOW2 = 2
FOLLOW3 = 3


MY_TURN = 0
OTHER_TURN = 1

DIAMOND = 0
CLUB = 1
HEART = 2
SPADE = 3

LESS = -1
EQUAL = 0
GREATER = 1

NOTHING = -1
STRAIGHT = 0 
FLUSH = 1 
FULL_HOUSE = 2
FOUR_OF_A_KIND = 3 
STRAIGHT_FLUSH = 4 

PROB_STRAIGTH = 0.00392465
PROB_FLUSH = 0.0019654
PROB_FULL_HOUSE = 0.00144058
PROB_FOUR_OF_A_KIND = 0.000240096
PROB_STRAIGHT_FLUSH = 0.0000138517

PROB_NB_STRAIGHT_FLUSH = (1.0- PROB_STRAIGHT_FLUSH)
PROB_NB_FOUR_OF_A_KIND = PROB_NB_STRAIGHT_FLUSH * (1.0-PROB_FOUR_OF_A_KIND)
PROB_NB_FULL_HOUSE = PROB_NB_FOUR_OF_A_KIND * (1.0 - PROB_FULL_HOUSE)
PROB_NB_FLUSH  = PROB_NB_FULL_HOUSE * (1.0 - PROB_FLUSH)
PROB_NB_STRAIGHT = PROB_NB_FLUSH * (1.0 - PROB_STRAIGTH)

NPC0_WIN = 0
NPC1_WIN = 1

NPC_LOOP = 5
SAMPLE_LOOP = 10
MCTS_LOOP = 10
TREE_SEARCH = 10
MCTS_OTHER_ROLE_LOOP = 40
MCTS_PLAY_LOOP = 1

NO_PLAY = 0
PREVIOUS_PLAY = 1
POST_PLAY = 2

ranks = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']
suits = ['D', 'C', 'H', 'S']

def get_rank(a):
  return a//4

def get_suit(a):
  return a%4

def get_longest_move_index(strategy):
  target_index = 0
  l = 0
  for i in range(len(strategy)):
    if len(strategy[i]) > l:
      l = len(strategy[i])
      target_index = i
  return target_index

def get_play_order(myId, toBeatId):
  if toBeatId == -1:
    return NO_PLAY
  if (toBeatId + 1)%4 == myId:
    return PREVIOUS_PLAY
  elif (myId + 1)%4 == toBeatId:
    return POST_PLAY

def split_moves_according_to_length(strategy):
  output = [[],[],[],[],[],[]]
  for move in strategy:
    output[len(move)].append(move)
  return output

def cal_move_length_in_strategy(strategy): #modify name,FIXME
  board = [0,0,0,0,0,0]
  for move in strategy:
    board[len(move)] += 1
  return board

def check_group2_is_greater_or_equal_than_group2(toBeCheck, strategy):
  l1 = len(toBeCheck)
  for s in strategy:
    l2 = len(s)
    if l1==l2:
      if l1 == 2:
        re = compare_two(toBeCheck, s)
        if re !=  LESS:
          pass
        else:
          return False
  return True

def check_group3_is_greater_or_equal_than_group3(toBeCheck, strategy):
  l1 = len(toBeCheck)
  for s in strategy:
    l2 = len(s)
    if l1==l2:
      if l1 == 3:
        re = compare_three(toBeCheck, s)
        if re !=  LESS:
          pass
        else:
          return False
  return True

def check_group4_is_greater_or_equal_than_group4(toBeCheck, strategy):
  l1 = len(toBeCheck)
  for s in strategy:
    l2 = len(s)
    if l1==l2:
      if l1 == 4:
        re = compare_four(toBeCheck, s)
        if re !=  LESS:
          pass
        else:
          return False
  return True

def func_strategy_compare(l, r):
  if len(l) < len(r):
    return LESS
  elif len(l) > len(r):
    return GREATER
  
  compare_two(l,r)

def select_all_length_n_moves(strategy, n):
  output  = []
  for move in strategy:
    if len(move) == n:
      output.append(move)
  return output

def sort_strategy(strategy):
  strategy = sorted(strategy, key = cmp_to_key(strategy_compare))
  return strategy

def strategy_of_length_n_number(strategy, n):
  t = 0
  for s in strategy:
    if len(s) == n:
      t+=1
  return t

def compare_one(a1, a2):
  rank1 = get_rank(a1[0])
  suit1 = get_suit(a1[0])
  rank2 = get_rank(a2[0])
  suit2 = get_suit(a2[0])
  if rank1 < rank2:
    return LESS
  elif rank1 > rank2:
    return GREATER
  elif suit1 < suit2:
    return LESS
  elif suit1 > suit2:
    return GREATER
  else:
    return EQUAL
  return EQUAL

#return a number represent the value of a pair, so that we can compare two pairs for which is bigger by this value
def cal_two_value(a):
  return max(a[0],a[1])

def compare_two(a1,a2):
  rank1 = get_rank(a1[0])
  suit1 = max(get_suit(a1[0]),get_suit(a1[1]))
  rank2 = get_rank(a2[0])
  suit2 = max(get_suit(a2[0]),get_suit(a2[1])) 
  if rank1 < rank2:
    return LESS
  elif rank1 > rank2:
    return GREATER
  elif suit1 < suit2:
    return LESS
  elif suit1 > suit2:
    return GREATER
  else:
    return EQUAL   
  
def cal_three_value(a):
  return get_rank(a[-1])

def compare_three(a1, a2):
  rank1 = get_rank(a1[0])
  rank2 = get_rank(a2[0])
  if rank1 < rank2:
    return LESS
  elif rank1 > rank2:
    return GREATER
  else:
    return EQUAL
  
def cal_four_value(a):
  return get_rank(a[-1])

def compare_four(a1, a2):
  rank1 = get_rank(a1)
  rank2 = get_rank(a2)
  if rank1 < rank2:
    return LESS
  elif rank1 > rank2:
    return GREATER
  else:
    return EQUAL
  
def compare_five(a1, a2):
  card_type1 = card5_type(a1)
  card_type2 = card5_type(a2)
  if card_type1 < card_type2:
    return LESS
  elif card_type1 > card_type2:
    return GREATER
  else:
    if card_type1 == STRAIGHT:
      return compare5_straight(a1,a2)
    elif card_type1 == FLUSH:
      return compare5_flush(a1,a2)
    elif card_type1 == FULL_HOUSE:
      return compare5_full_house(a1,a2)
    elif card_type1 == FOUR_OF_A_KIND:
      return compare5_four_of_a_kind(a1,a2)
    elif card_type1 == STRAIGHT_FLUSH:
      return compare5_straight_flush(a1,a2)
    else:
      print("card5_type_nothing!\n")
      raise Exception("card5_type_nothing!\n")  

def strategy_compare(a1, a2):
  if len(a1) < len(a2):
    return LESS
  elif len(a1) > len(a2):
    return GREATER
  
  length = len(a1)
  if length == 1:
    return compare_one(a1,a2)
  elif length == 2:
    return compare_two(a1,a2)
  elif length == 3:
    return compare_three(a1,a2)
  elif length == 5:
    return compare_five(a1,a2)

  return EQUAL
 
def compare(a1,a2):
  if len(a1) != len(a2):
    print("compare_unequal_length\n")
    raise Exception("compare_unequal_length\n")
  
  length = len(a1)
  if length == 1:
    return compare_one(a1,a2)
  elif length == 2:
    return compare_two(a1,a2)
  elif length == 3:
    return compare_three(a1,a2)
  elif length == 5:
    return compare_five(a1,a2)

  print("compare_unequal_length\n")
  raise Exception("compare_unequal_length\n")

def toNumber(card):
  return ranks.index(card[0])*4+suits.index(card[1])

def toCharacter(card):
  rank = get_rank(card)
  suit = get_suit(card)
  return f'{ranks[rank]}{suits[suit]}'

def transform_in(myHand):
  output = []
  for i in range(len(myHand)):
      card = myHand[i]
      id = ranks.index(card[0])*4+suits.index(card[1])
      output.append(id)
  output = sorted(output)
  return output

def transform_out(cards):
  output = []
  for i in range(len(cards)):
    card = cards[i]
    rank = get_rank(card)
    suit = get_suit(card)
    output.append(f'{ranks[rank]}{suits[suit]}')
  return output

def cal_box_value(box):
  return -len(box) #FIXME

def sort_box(box):
  return sorted(box, key=len)

def transform_box_number_to_box_character(box):
  output = []
  for i in range(len(box)):
    output.append([])
    for j in range(len(box[i])):
      output[i].append([])
      for k in range(len(box[i][j])):
        rank=  get_rank(box[i][j][k])
        suit = get_suit(box[i][j][k])
        output[i][j].append(f'{ranks[rank]}{suits[suit]}')
  return output


def sub_cards(handCards, move):
  output = []
  for hand in handCards:
    bingo = False
    for m in move:
      if hand == m:
        bingo = True
        break
    if bingo == False:
      output.append(hand)
  return output

#divide hand cards according to ranks
def make_hand_group(myHandCards):
  handGroup = []
  group = []
  for i in range(len(myHandCards)):
    if len(group)==0 or get_rank(myHandCards[i])==get_rank(group[0]):
      group.append(myHandCards[i])
    else:
      handGroup.append(copy.deepcopy(group))
      group = [myHandCards[i]]
  if len(group) > 0:
    handGroup.append(group)
  return handGroup

#dividing handcards according to suit
def make_flush_group(myHandCards):
  myFlushGroup = [[],[],[],[]] #group according to suit
  for i in range(len(myHandCards)):
    suit = get_suit(myHandCards[i])
    myFlushGroup[suit].append(myHandCards[i])
  return myFlushGroup

def create_ordered_cards():
  cards = [0] * 52
  for i in range(0,52):
    cards[i] = i
  return cards 

def create_shuffled_cards():
  cards = create_ordered_cards()
  random.shuffle(cards)
  return cards

def compare5_straight(left, right):
  if left[4] < right[4]:
    return LESS 
  elif left[4] > right[4]:
    return GREATER
  else:
    return EQUAL

def compare5_flush(left, right):
  left_keys = [get_suit(l) for l in left] + [get_rank(l) for l in left]
  right_keys = [get_suit(l) for l in right] + [get_rank(l) for l in right]
  for i in range(9,-1,-1):
    if left_keys[i] < right_keys[i]:
      return LESS
    elif left_keys[i] > right_keys[i]:
      return GREATER
    
  return EQUAL

def compare5_four_of_a_kind(left, right):
  if (left[1]%4)==0:
    l = left[4]
  else:
    l = left[3] 
  if (right[1]%4)==0:
    r = right[4] 
  else:
    r = right[3]
  if l < r:
    return LESS
  elif l > r:
    return GREATER
  return EQUAL

def compare5_full_house(left,right):
  if left[2]//4 == left[1]//4:
    l = left[2]
  else:
    l = left[4]
  if right[2]//4 == right[1]//4:
    r = right[2]
  else:
    r = right[4]
  if get_rank(l) < get_rank(r):
    return LESS
  elif get_rank(l) > get_rank(r):
    return GREATER
  
  return EQUAL

def compare5_straight_flush(left, right):
  if (left[4] < right[4]):
    return LESS
  elif (left[4] > right[4]):
    return GREATER
  return EQUAL 

#find the index of the first element which is bigger
def binary_search(composites, composite, compare_func):
  if(len(composites) >= 2):
    index = len(composites)//2
    re =  compare_func(composites[index-1], composite)
    if re == LESS:
      return index - 1 + binary_search(composites[index :], composite, compare_func)
    elif re == GREATER:
      return binary_search(composites[0 : index-1], composite, compare_func)
    else:
      #find the index of the rightmost equal element
      for i in range(index +1 , len(composites), 1):
        if compare_func(composites[i],composite) == EQUAL:
          index += 1
        else:
          return (i-1)
      return index
      
  elif len(composites) == 1:
    re = compare_func(composites[0], composite)
    if re == EQUAL:
      return 0
    else:
      return -1
  else:
    return -1
  
  return -1

def get_full_house_trump_cards(full_house):
  if get_rank(full_house[0]) == get_rank(full_house[1]) and get_rank(full_house[1])==get_rank(full_house[2]):
    return [full_house[0],full_house[1],full_house[2]]
  else:
    return [full_house[2],full_house[3],full_house[4]]


def card5_type(sorted_cards):
  card_type = NOTHING
  ranks = [get_rank(card) for card in sorted_cards]
  if ranks[1] == ranks[0]+1 and ranks[2] == ranks[1]+1 and ranks[3] == ranks[2]+1 and ranks[4] == ranks[3] + 1:
    card_type = STRAIGHT
    suits = [get_suit(card) for card in sorted_cards]
    if suits[0]==suits[1] and suits[0] == suits[2] and suits[0]==suits[3] and suits[0] == suits[4]:
      card_type = STRAIGHT_FLUSH
    return card_type
  
  if (ranks[0]==ranks[1] and ranks[0]==ranks[2] and ranks[0]==ranks[3]) or (ranks[1]==ranks[2] and ranks[2]== ranks[3] and ranks[3]==ranks[4]):
    card_type = FOUR_OF_A_KIND
    return card_type
  
  if((ranks[0] == ranks[1] and ranks[0] == ranks[2] and ranks[3]== ranks[4]) or (ranks[0]==ranks[1] and ranks[2]==ranks[3] and ranks[3] == ranks[4])):
    card_type = FULL_HOUSE
    return card_type
  
  suits = [get_suit(card) for card in sorted_cards]
  if(suits[0]==suits[1] and suits[1]==suits[2] and suits[2]==suits[3] and suits[3]==suits[4]):
    card_type = FLUSH 
    return card_type

  return card_type

def find_card_index(rank, suit):
  return rank * 4 + suit 

def find_all_straight_and_straight_flush():
  all_straight = []
  all_straight_flush = []
  for last in range(20, 53, 4):
    for s4 in range(last-4,last):
      for s3 in range(last-8, last-4):
        for s2 in range(last-12, last-8):
          for s1 in range(last-16, last-12):
            for s0 in range(last-20, last-16):
              suit0 = get_suit(s0)
              suit1 = get_suit(s1)
              suit2 = get_suit(s2)
              suit3 = get_suit(s3)
              suit4 = get_suit(s4)
              if(suit0==suit1 and suit0==suit2 and suit0 == suit3 and suit0 == suit4):
                all_straight_flush.append((s0,s1,s2,s3,s4))
              else:
                all_straight.append((s0,s1,s2,s3,s4))
  return all_straight, all_straight_flush

def find_all_four_of_a_kind():
  all_four_of_a_kind = []
  for start in range(0, 52, 4):
    for another in range(0,52):
      if another < start:
        all_four_of_a_kind.append((another,start,start+1,start+2,start+3))
      elif another >= (start + 4):
        all_four_of_a_kind.append((start,start+1,start+2,start+3,another))
  return all_four_of_a_kind

def find_all_full_house():
  all_full_house = []
  for start in range(0,52,4):
    for s2 in range(start+2,start+4):
      for s1 in range(start+1, s2 ,1):
        for s0 in range(start, s1):
          for last in range(0,52, 4):
            if last != start:
              for t2 in range(last+1,last+4):
                for t1 in range(last, t2):
                  if t2 < s0:
                    all_full_house.append((t1,t2,s0,s1,s2))
                  else:
                    all_full_house.append((s0,s1,s2,t1,t2))
  return all_full_house

  
def find_all_flush():
  all_flush = []
  for s4 in range(0, 52):
    offset = s4%4
    for s3 in range(offset,s4,4):
      for s2 in range(offset, s3, 4):
        for s1 in range(offset, s2, 4):
          for s0 in range(offset,s1, 4):
            if (s4 - s0 > 16):
              all_flush.append((s0,s1,s2,s3,s4))
            else:
              #here is straight_flush
              pass
  return all_flush

def calculate_value(times, win):
  value = 0
  if win == NPC0_WIN:
    value += 10
    value -= times
  elif win == NPC1_WIN:
    value += times
  return value

def cal_min_num_cards(leftOvers):
  mi = 13
  for i in range(len(leftOvers)):
    if mi > leftOvers[i]:
      mi = leftOvers[i]
  return mi

def choose_from_one_strategy_new(strategy, other_hands, leftOvers, myPlayerId):
  npc = NewNPC()

  otherHandGroup = make_hand_group(other_hands)

  sg = sort_strategy(strategy)
  move_count = len(sg)

  splits = split_moves_according_to_length(sg)

  
  moveLengths = cal_move_length_in_strategy(sg)
  
  move_count = len(sg)

  minNumCardInOtherHand = cal_min_num_cards(leftOvers)
  #in this case we can only play backward
  if minNumCardInOtherHand == 1:
    for move in splits[2]:
      return move
    for move in splits[3]:
      return move
    for move in splits[5]:
      return move
    for j in range(len(splits[1])-1,-1,-1):
      return splits[1][j]

  #strategy1: if i have a five and two single, if the bigger single is not big enough
  #play the five, else play the small single
  if moveLengths[5] == 1:
    if moveLengths[1] == 2 and  move_count ==3:
      re = compare_one(splits[1][-1], [other_hands[-1]])
      if re == GREATER:
        return splits[1][0]
      else:
        return splits[5][0]
    elif moveLengths[1] == 1 and move_count ==2:
      re = compare_one(splits[1][-1], [other_hands[-1]])
      if re == GREATER:
        return splits[1][0]
      else:
        return splits[5][0]

  #only singles and pairs, decide which to play
  if moveLengths[3] == 0 and moveLengths[5] == 0 and moveLengths[1]>0 and moveLengths[2]>0:
    #if the pairs are very big, say 2H,2S, probably i would play singles with pairs
    p1 = npc.probability_of_bigger_one_not_exist([splits[2][-1][-1]],other_hands,leftOvers)
    p2 = npc.probability_of_bigger_one_not_exist([splits[2][-1][-2]],other_hands,leftOvers)
    if p1 * p2 > 0.9:
      return splits[1][0]
    
    # if I have lots of pairs but only a small single, definitly I'll play pairs
    q2 = npc.probability_of_bigger_pair_not_exist(splits[2][-1], otherHandGroup, leftOvers)
    q1 = npc.probability_of_bigger_one_not_exist(splits[1][-1], other_hands, leftOvers)
    if q2 > q1:
      return splits[2][0]
    else: 
      return splits[1][0]

    d = splits[1][-1][0] - other_hands[-1]
    if d > 0:
      return splits[1][0]
    d2 = get_rank(splits[2][-1][1])
    two_groups = npc.cal_two_cards(other_hands)
    if len(two_groups) == 0:
      return splits[2][-1]
    else:
      if compare_two(splits[2][-1], two_groups[-1]) == GREATER:
        return splits[2][0]
      elif get_rank(two_groups[-1][0]) - get_rank(splits[2][-1][0]) <= 2:
        return splits[2][0]
    return splits[1][0]

  #only singles and threes
  if moveLengths[2] == 0 and moveLengths[5] == 0 and moveLengths[1] > 0 and moveLengths[3] > 0:
    p1 = npc.probability_of_bigger_three_not_exist(splits[3][-1],otherHandGroup, leftOvers)
    p2 = npc.probability_of_bigger_one_not_exist(splits[1][-1], other_hands, leftOvers)
    if p2 > p1:
      return splits[1][0]
    else:
      return splits[3][0]
    
  #full_hose and singles 
  if moveLengths[1]>=2 and moveLengths[5]==1 and moveLengths[2] ==0 and moveLengths[3] == 0:
    tp = card5_type(splits[5][0])
    if tp == FULL_HOUSE:
      trump_cards = get_full_house_trump_cards(splits[5][0])
      p1 = npc.probability_of_bigger_one_not_exist([trump_cards[-1]],other_hands, leftOvers)
      p2 = npc.probability_of_bigger_one_not_exist([trump_cards[-2]], other_hands, leftOvers)
      p3 = npc.probability_of_bigger_one_not_exist([trump_cards[-3]], other_hands, leftOvers)
      if p1 * p2 * p3 >= 0.9:
        return splits[1][0]

  #singles and fives (twos and threes possible):
  if moveLengths[1] >= 1 and moveLengths[5] >= 1:
    pass
      
  #only singles
  if moveLengths[1]>0 and moveLengths[5]==0 and moveLengths[2] ==0 and moveLengths[3] == 0:
    if moveLengths[1] <= 2 and (leftOvers[0] == 1 or leftOvers[1] == 1 or leftOvers[2] == 1):
     return splits[1][-1]
    else:
     return splits[1][0]

  choice = random.randint(0, move_count-1)
  #return sg[choice]
  index = get_longest_move_index(sg)
  return sg[index]



class Table:
  def __init__(self):
    self.all_straight, self.all_straight_flush = find_all_straight_and_straight_flush()
    self.all_four_of_a_kind = find_all_four_of_a_kind()
    self.all_full_house = find_all_full_house()
    self.all_flush = find_all_flush()


def get_other_cards(cards):
  output = []
  for i in range(len(cards)):
    if cards[i]==IN_OTHER_HAND:
      output.append(i)
  return output


######################helper-end###################

#############################npc#####################

#Monte Carlo tree search

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
          output.append([i])
    else:
      card = cards[0]
      for i in range(card + 1,52):
        if self.card_state[i] == IN_MY_HAND:
          output.append([i])
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
              output.append([i,j])
    return output
      
  def cal_three_cards_moves(self, cards):
    output = []
    if cards == None or len(cards)==0 :
      rank = 0
      l = 3
    else:
      rank = get_rank(cards[0])
      l = rank+4 - (rank%4) +3
    for i in range(l, 52, 4):
      if(self.card_state[i-3]==IN_MY_HAND
          and self.card_state[i-2]==IN_MY_HAND
          and self.card_state[i-1]==IN_MY_HAND):
        output.append([i-1,i-2,i-3])
      if(self.card_state[i] == IN_MY_HAND
          and self.card_state[i-3]==IN_MY_HAND
          and self.card_state[i-2] == IN_MY_HAND):
        output.append([i, i-2,i-3])
      if(self.card_state[i] == IN_MY_HAND
          and self.card_state[i-3] == IN_MY_HAND
          and self.card_state[i-1] == IN_MY_HAND):
        output.append([i,i-3,i-1])
      if(self.card_state[i] == IN_MY_HAND
          and self.card_state[i-1] == IN_MY_HAND
          and self.card_state[i-2] == IN_MY_HAND):
        output.append([i,i-1,i-2])
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
          return [flushGroup[i][j-4:j+1]] #FIXED

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
    return output
              
  
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

  def make_handGroup(self):
    myHandGroup = [] #group according to rank
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

    return myHandGroup 
  
  def make_flushGroup(self):
    myFlushGroup = [] #group according to suit
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

    return myFlushGroup

  def cal_5card_possible_moves_new(self, toBeat):
    #group according to rank
    myHandGroup = self.make_handGroup()
    #group according to suit
    myFlushGroup = self.make_flushGroup()

    output = []
    if toBeat == None or len(toBeat) == 0:
      output += self.cal_straight_new(myHandGroup, toBeat)
      output += self.cal_flush_new(myFlushGroup, toBeat)
      output += self.cal_full_house_new(myHandGroup, toBeat)
      output += self.cal_four_in_a_kind_new(myHandGroup, toBeat)
      output += self.cal_straight_flush_new(myFlushGroup, toBeat)
      return output
     
    toBeat = sorted(toBeat)
    type = card5_type(toBeat)
    if type == STRAIGHT:
      output += self.cal_straight_new(myHandGroup, toBeat)
      output += self.cal_flush_new(myFlushGroup, [])
      output += self.cal_full_house_new(myHandGroup, [])
      output += self.cal_four_in_a_kind_new(myHandGroup, [])
      output += self.cal_straight_flush_new(myFlushGroup, [])
    elif type == FLUSH:
      output += self.cal_flush_new(myFlushGroup, toBeat)
      output += self.cal_full_house_new(myHandGroup, [])
      output += self.cal_four_in_a_kind_new(myHandGroup, [])
      output += self.cal_straight_flush_new(myFlushGroup, [])
    elif type == FULL_HOUSE:
      output += self.cal_full_house_new(myHandGroup, toBeat)
      output += self.cal_four_in_a_kind_new(myHandGroup, [])
      output += self.cal_straight_flush_new(myFlushGroup, [])
    elif type == FOUR_OF_A_KIND:
      output += self.cal_four_in_a_kind_new(myHandGroup, toBeat)
      output += self.cal_straight_flush_new(myFlushGroup, [])
    elif type == STRAIGHT_FLUSH:
      output += self.cal_straight_flush_new(myFlushGroup, toBeat)

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
  
  def cal_good_compositions(self, myHand):
    handGroup = self.make_handGroup()
    flushGroup = self.make_flushGroup()
    compositions = []
    
    self.deep_call(myHand, compositions)
    return compositions

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
  
  def cal_good_selfplay_moves(self):
    output = []
    handGroup = self.make_handGroup()
    flushGroup = self.make_flushGroup()
    flushes = self.cal_flush_new(flushGroup, [])
    straights = self.cal_straight_new(handGroup, [])
      
    for group in handGroup:
      if (len(group) == 1): 
        not_in_any_straight = True
        for straight in straights:
          if group[0] in straight:
            not_in_any_straight = False
            break
        not_in_any_flush = True
        for flush in flushes:
          if group[0] in flush:
            not_in_any_flush = False
            break 
        if not_in_any_straight and not_in_any_flush:
          return [group]

    #if it comes here, that means no single, so
    output += self.cal_two_cards_moves(None)
    output += self.cal_three_cards_moves(None)
    output += self.cal_full_house_new(handGroup, [])
    output += self.cal_four_in_a_kind_new(handGroup, [])
    output += self.cal_straight_flush_new(handGroup, [])

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

  




###############################npc-end############


class PlayInfo:
  def __init__(self):
    self.myHandCards = []
    self.otherHands = []
    self.toBeat = []
    self.myPlayerNum = 0
    self.leftOvers = []
    self.toBeatId = -1
    self.first_round_first_play = False
    self.simulate = False

###################algorithm##################

class Algorithm:

    def __init__(self):
      pass

    def sort_and_transform_by_color(self, cards):
      rt = copy.deepcopy(cards)
      fours = [[],[],[],[]]
      for card in cards:
        if get_suit(card)== DIAMOND:
          fours[0].append(card)
        elif get_suit(card) == CLUB:
          fours[1].append(card)
        elif get_suit(card) == HEART:
          fours[2].append(card)
        elif get_suit(card) == SPADE:
          fours[3].append(card)
      js = []
      for four in fours:
        if(len(four)>=5):
          js.append(transform_out(four))
      return js


    def getAction(self, state: MatchState):
      newNpc = NewNPC()

      myHandCards = transform_in(state.myHand)

      toBeat = []
      if state.toBeat == None:
        toBeat = []
      else: 
        toBeat = transform_in(state.toBeat.cards)

      action = []             # The cards you are playing for this trick
      myData = state.myData   # Communications from the previous iteration

      
      if(len(state.matchHistory) == 0):
        print("len(state.matchHistory)==0!\n")
        return action, myData 
      
      gameHistory = state.matchHistory[-1]
      rounds = gameHistory.gameHistory
      played_cards = []
      for i in range(len(rounds)):
        for trick in rounds[i]:
          played_cards += transform_in(trick.cards)

      #get previous player info
      toBeatId = -1
      if(len(rounds)==0):
        pass
      else:
        for trick in rounds[-1]:
          cards = transform_in(trick.cards)
          if cards == toBeat:
            toBeatId = trick.playerNum
            break

      first_round_first_play = False
      if len(rounds)==0 and len(toBeat) == 0:
        #in this case, must be i am first:
        first_round_first_play = True
        print("first_round_first_play\n")

      #new game start
      if len(myData) == 0:
        newNpc.current_folder_time = 0
      else:
        newNpc.current_folder_time = int(myData)
      if len(rounds) == 0 or (len(rounds)==1 and len(rounds[0])<=3):
        print("New Game Start?\n")
        newNpc.current_folder_time = 0
      print(f"Folder_Time:{newNpc.current_folder_time}\n")

      #formulate the state:
      card_state = [IN_OTHER_HAND] * 52
      for card in played_cards:
        card_state[card] = CARD_PLAYED
      for card in myHandCards:
        card_state[card] = IN_MY_HAND
      other_hands = []
      for i in range(52):
        if card_state[i] == IN_OTHER_HAND:
          other_hands.append(i)


      print(f"{VERSION}_id\n")
      print(f"myPlayerNum = {state.myPlayerNum}\n")
      print(f"toBeatId = {toBeatId}\n")
      print(f"myHands = {transform_out(sorted(myHandCards))}\n")
      print(f"myHandsColor = {self.sort_and_transform_by_color(myHandCards)}\n")
      print(f"toBeat = {transform_out(toBeat)}\n")
      print(f"otherHands = {transform_out(other_hands)}\n")
      print(f"handSize = {[state.players[0].handSize,state.players[1].handSize,state.players[2].handSize,state.players[3].handSize]}\n")

      leftOvers = newNpc.cal_otherHands_numbers(state.myPlayerNum, state.players)

      playInfo = PlayInfo()
      playInfo.first_round_first_play = first_round_first_play
      playInfo.leftOvers = leftOvers
      playInfo.myHandCards = myHandCards
      playInfo.otherHands = other_hands
      playInfo.toBeat = toBeat
      playInfo.toBeatId = toBeatId
      playInfo.simulate = False
      playInfo.myPlayerNum = state.myPlayerNum

      return newNpc.play_card(playInfo, myData)
    

class NewNPC: 
  def __init__(self):
    
    self.current_folder_time = 0
    pass 
  
  def merge_moves_in_each_strategy(self, box):
    for i in range(len(box)):
      mid = box[i]
      box[i] = []
      splits = split_moves_according_to_length(mid)
      l2 = len(splits[2])
      l3 = len(splits[3])
      l4 = len(splits[4])
      l1 = len(splits[1])
      l5 = len(splits[5])

      for j in range(min(l1,l4)):
        box[i].append(sorted(splits[1][j]+splits[4][j]))
      if l1 > l4:
        for j in range(l4,l1):
          box[i].append(splits[1][j])
      elif l4 > l1:
        for j in range(l1,l4):
          box[i].append(splits[4][j])


      for t in splits[5]:
        box[i].append(t)


      #without merge 2,3 
      exist_3_2_merge = min(l2,l3) > 0
      if exist_3_2_merge == True:
        mid = sorted(mid)
        box.append(mid)

      
      for j in range(min(l2,l3)):
        box[i].append(sorted(splits[2][j]+splits[3][j]))
      if l3 > l2:
        for j in range(l2, l3):
          box[i].append(splits[3][j])
      if l3 < l2:
        for j in range(l3,l2):
          box[i].append(splits[2][j])

      
      box[i] = sort_strategy(box[i])
    return 

  #myPair, the pair in my hand, like [6D,6H]
  #handGroup, like [[3D,3H,3S],[6C,6S],[9D,9C,9H,9S]]
  #leftOvers, cards number in each hand: [3,4,5]
  def probability_of_bigger_pair_not_exist(self, myPair, otherHandGroup, LeftOvers):
    leftOvers = copy.deepcopy(LeftOvers)
    leftOverLen = len(leftOvers)
    start = 0
    for i in range(len(otherHandGroup)):
      if otherHandGroup[i][-1] >= myPair[-1]:
        start = i
        break
    p = 1.0
    for i in range(start+1, len(otherHandGroup)):
      if len(otherHandGroup[i]) == 4:
        return 0.0
      
    numbers_of_zero_in_leftOvers = 0
    for i in range(start+1, len(otherHandGroup)):
      if len(otherHandGroup[i])==3:
        if leftOvers[0] == 0 or leftOvers[1] == 0 or leftOvers[2] == 0:
          if(leftOvers[0]==0 and leftOvers[1]==0 and leftOvers[2]==0):
            return p
          else:
            return 0.0
        length = leftOvers[0]+leftOvers[1]+leftOvers[2]
        p_not_together = float(leftOvers[0]*leftOvers[1]*leftOvers[2]) * 6/float(length*(length-1)*(length-2))
        p = p * p_not_together
        leftOvers[0]-=1
        leftOvers[1]-=1
        leftOvers[2]-=1
    
    for i in range(start+1, len(otherHandGroup)):
      if len(otherHandGroup[i]) == 2:
        length = leftOvers[0]+leftOvers[1]+leftOvers[2]
        p_not_together = float(leftOvers[0]*leftOvers[1] + leftOvers[0]*leftOvers[2] +leftOvers[1]*leftOvers[2]) * 2/float(length * (length-1))
        p = p * p_not_together
        #here is an approximate
    
    if(len(otherHandGroup[start])==2):
      if otherHandGroup[start][-1] < myPair[-1]:
        pass 
      else:
        length = leftOvers[0]+leftOvers[1]+leftOvers[2]
        p = p * float(LeftOvers[0]*LeftOvers[1] + LeftOvers[0]*LeftOvers[2] +LeftOvers[1]*LeftOvers[2]) * 2/float(length * (length-1))

    return p
  
  
  def probability_of_bigger_three_not_exist(self, myThree, otherHandGroup, leftOvers):
    p = 1.0
    start = 0
    #this is jus an approximate calculation
    for i in range(0, len(otherHandGroup)):
      if otherHandGroup[i][-1] > myThree[-1]:
        start = i
        break
    
    length = leftOvers[0]+leftOvers[1]+leftOvers[2]
    for i in range(start, len(otherHandGroup)):
      if len(otherHandGroup[i])==3:
        p_together=  0.0
        if leftOvers[0]>=3:
          p_together += float(leftOvers[0]*(leftOvers[0]-1)*(leftOvers[0]-2)/6)
        if leftOvers[1]>=3:
          p_together += float(leftOvers[1]*(leftOvers[1]-1)*(leftOvers[1]-2)/6)
        if leftOvers[2]>=3:
          p_together += float(leftOvers[2]*(leftOvers[2]-1)*(leftOvers[2]-2)/6)
        
        p_together = p_together/float(length*(length-1)*(length-2)/6)
        p_not_together = 1.0 - p_together
        p = p * p_not_together
      elif len(otherHandGroup[i]) == 4:
        p_4_in_one = 0.0
        denomitor = float(length * (length-1)*(length-2)*(length-3))/24
        if(leftOvers[0]>=4):
          p_4_in_one += float(leftOvers[0]*(leftOvers[0]-1)*(leftOvers[0]-2)*(leftOvers[0]-3))/24/denomitor
        if(leftOvers[1]>=4):
          p_4_in_one += float(leftOvers[1]*(leftOvers[1]-1)*(leftOvers[1]-2)*(leftOvers[1]-3))/24/denomitor
        if(leftOvers[1]>=4):
          p_4_in_one += float(leftOvers[2]*(leftOvers[2]-1)*(leftOvers[2]-2)*(leftOvers[2]-3))/24/denomitor
        p_3_in_one = 0.0
        if(leftOvers[0]>=3):
          p_3_in_one += float(leftOvers[0]*(leftOvers[0]-1)*leftOvers[0]-2)/6 * leftOvers[1] * leftOvers[2]/denomitor
        if(leftOvers[1]>=3):
          p_3_in_one += float(leftOvers[1]*(leftOvers[1]-1)*leftOvers[1]-2)/6 * leftOvers[0] * leftOvers[2]/denomitor
        if(leftOvers[2]>=3):
          p_3_in_one += float(leftOvers[2]*(leftOvers[2]-1)*leftOvers[2]-2)/6 * leftOvers[0] * leftOvers[1]/denomitor
        p_not_together=  1.0 - (p_4_in_one + p_3_in_one)
        p = p * p_not_together

    return p

  def probability_of_bigger_five_not_exist(self, myFive, otherHandGroup, leftOvers):
    if leftOvers[0]<5 and leftOvers[1]<5 and leftOvers[2]<5:
      return 1.0
    #a very rough approximate formula
    tp = card5_type(myFive)
    if tp == STRAIGHT:
      return PROB_NB_STRAIGHT
    elif tp == FLUSH:
      return PROB_NB_FLUSH
    elif tp == FULL_HOUSE:
      return PROB_NB_FULL_HOUSE
    elif tp == FOUR_OF_A_KIND:
      return PROB_NB_FOUR_OF_A_KIND
    elif tp == STRAIGHT_FLUSH:
      return PROB_NB_STRAIGHT_FLUSH

    return 1.0
    
  def probability_of_bigger_one_not_exist(self, myOne, otherHands, leftOvers):
    if myOne[0] > otherHands[-1]:
      return 1.0 
    else:
      return 0.0
      #return myOne[0]/otherHands[-1]
    return 1.0

  # def mc_play_one_card_by_smallest_strategy(self, cards, toBeat):
  #   rt = []
  #   for i in range(len(cards)):
  #     if cards[i][0] > toBeat[0]:
  #       rt = cards[i]
  #       del cards[i]
  #       return rt, True
  #   return toBeat, False

  # def npc_play_one_cards_by_random_strategy(self, cards, toBeat):
  #   return False

  # def mc_play_two_cards_by_smallest_strategy(self, cards, toBeat):
  #   return False

  # def npc_play_two_cards_by_random_strategy(self,cards, toBeat):
  #   return False

  # def mc_play_three_cards_by_smallest_strategy(self, cards, toBeat):
  #   return False

  # def npc_play_three_cards_by_random_strategy(self, cards, toBeat):
  #   return False

  # def cal_strategy_value_by_mcts(self, strategy, otherHands, otherHandsGroup, leftOvers):
  #   splits = split_moves_according_to_length(strategy)
  #   p = 1.0

  #   seed_value = int(time.time())
  #   random.seed(seed_value)


  #   for i in range(MCTS_OTHER_ROLE_LOOP):
  #     otherHandsCpy = copy.deepcopy(otherHands)
  #     random.shuffle(otherHandsCpy)
  #     hd0_1 = copy.deepcopy(splits[1])
  #     hd0_2 = copy.deepcopy(splits[2])
  #     hd0_3 = copy.deepcopy(splits[3])
  #     hd1 = make_hand_group(sorted(otherHandsCpy[0:leftOvers[0]]))
  #     hd2 = make_hand_group(sorted(otherHandsCpy[leftOvers[0]:leftOvers[1]]))
  #     hd3 = make_hand_group(sorted(otherHandsCpy[leftOvers[1]:leftOvers[2]]))

  #     if len(splits[1])> 0:
  #       not_finish = True 
  #       toBeat = []
  #       acc_fail = 0
  #       ar = [hd0_1,hd1,hd2,hd3]
  #       i = 0
  #       while not_finish:
  #         toBeat,suc = self.mc_play_one_card_by_smallest_strategy(ar[i], toBeat)
  #         i = (i+1)%4
  #         if suc == False:
  #           acc_fail += 1
  #           if acc_fail == 3:
  #             break
  #         else:
  #           acc_fail = 0
  #         toBeat = self.npc_play_one_cards_by_random_strategy(hd1, toBeat)
  #         toBeat = self.npc_play_one_cards_by_random_strategy(hd2, toBeat)
  #         toBeat = self.npc_play_one_cards_by_random_strategy(hd3, toBeat)
        
  #     if len(splits[2]) > 0:
  #       pass
  #     if len(splits[3]) > 0:
  #       pass
  #   return 
  
  def cal_one_cards_expectation_length(self, split, otherHands):
    if len(split) == 0 or len(otherHands) == 0:
      return 0.0 

    #now we do sorting
    ones = []
    for i in range(len(otherHands)):
      ones.append([otherHands[i]])

    for i in range(len(split)//2, len(split)):
      ones.append(split[i])

    ones = sorted(ones, key = cmp_to_key(compare_one))

    fracs = []
    for i in range(len(split)//2, len(split)):
      for j in range(len(ones)):
        if split[i] == ones[j]:
          fracs.append(float(j+1)/len(ones))
          ones.remove(ones[j])
          break
    
    expl = 1.0
    for i in range(len(fracs)-1, -1, -1):
      if fracs[i] >= 0.9999:
        expl += 2.0
    if expl > len(split):
      expl = len(split)
    
    return expl
  
  #a very extremly formula, to be optimized (FIX ME)
  def cal_two_cards_expectation_length(self, split, otherHands, otherHandsGroup, leftOvers):
    if len(split) == 0 or len(otherHands) == 0:
      return 0.0 

    #now we do sorting
    pairs = []
    for i in range(len(otherHandsGroup)):
      if len(otherHandsGroup[i]) == 2:
        pairs.append(otherHandsGroup[i])
      elif len(otherHandsGroup[i]) == 3:
        pairs.append(otherHandsGroup[i][1:3])
      elif len(otherHandsGroup[i]) == 4:
        pairs.append(otherHandsGroup[i][2:4])

    for i in range(len(split)//2, len(split)):
      pairs.append(split[i])

    pairs = sorted(pairs, key = cmp_to_key(compare_two))

    fracs = []
    for i in range(len(split)//2, len(split)):
      for j in range(len(pairs)):
        if split[i] == pairs[j]:
          fracs.append(float(j+1)/len(pairs))
          pairs.remove(pairs[j])
          break
    
    expl = 2
    for i in range(len(fracs)-1, -1, -1):
      if fracs[i] >= 0.9999:
        expl += 4
    if expl > len(split) * 2:
      expl = len(split) * 2
    
    return expl

  def cal_three_cards_expectation_length(self, split, otherHands, otherHandsGroup, leftOvers):
    if len(split) == 0 or len(otherHands) == 0:
      return 0.0 

    #now we do sorting
    threes = []
    for i in range(len(otherHandsGroup)):
      if len(otherHandsGroup[i]) == 3:
        threes.append(otherHandsGroup[i])
      elif len(otherHandsGroup[i]) == 4:
        threes.append(otherHandsGroup[i][2:4])

    for i in range(len(split)//2, len(split)):
      threes.append(split[i])

    threes = sorted(threes, key = cmp_to_key(compare_three))

    fracs = []
    for i in range(len(split)//2, len(split)):
      for j in range(len(threes)):
        if split[i] == threes[j]:
          fracs.append(float(j+1)/len(threes))
          threes.remove(threes[j])
          break

    expl = 3.0
    for i in range(len(fracs)-1, -1, -1):
      if fracs[i] >= 0.9999:
        expl += 3.0 * 2
    if expl > len(split) * 3.0:
      expl = len(split) * 3.0
    
    return expl
  
  def cal_strategy_expectation_length(self, strategy, otherHands, otherHandsGroup, leftOvers):
    splits = split_moves_according_to_length(strategy)
    expl = 0.0
    if len(splits[1]) > 0:
      expl += self.cal_one_cards_expectation_length(splits[1], otherHands)
    if len(splits[2]) > 0:
      expl += self.cal_two_cards_expectation_length(splits[2], otherHands, otherHandsGroup,leftOvers )
    if len(splits[3]) > 0:
      expl += self.cal_three_cards_expectation_length(splits[3], otherHands, otherHandsGroup, leftOvers)
    if len(splits[5])>0:
      expl += 5.0 * len(splits[5]) #FIXME
    return expl
  

  def cal_strategy_value(self, strategy, otherHands, otherHandsGroup, otherHandNumbers):
    splits = split_moves_according_to_length(strategy)
    #calculate value of each split
    #the value of this strategy is the product of the probability of no beat

    p = 1.0
    #calculate 1-card move values:
    #lowest,[otherhands],highest,[otherhands]
    other_len = len(otherHands)
    if len(splits[1])> 0:
      l = len(splits[1])
      ind = -1
      #a simple formula to count the probablity of play all single cards
      while l > 0 and (-ind)<=other_len:
        myMax = splits[1][ind][0]
        if myMax < otherHands[ind]:
          p *= float(myMax)/float(otherHands[ind])
        l-=2
        ind -= 1
    if len(splits[2])> 0:
      l = len(splits[2])
      ind = -1
      while l > 0:
        p *= self.probability_of_bigger_pair_not_exist(splits[2][ind],otherHandsGroup,otherHandNumbers )
        ind -= 1
        l -= 2
    if len(splits[3])> 0:
      l = len(splits[3])
      ind = -1
      while l > 0:
        p *= self.probability_of_bigger_three_not_exist(splits[3][ind], otherHandsGroup, otherHandNumbers)
        ind -= 1
        l -= 2
    if len(splits[5])>0:
      l = len(splits[5])
      ind = -1
      while l > 0:
        p *= self.probability_of_bigger_five_not_exist(splits[5][ind], otherHandsGroup, otherHandNumbers)
        ind -= 1
        l -= 2

    return p


  def sort_box_by_value(self, box_with_value, reverse = False):
    box_with_value = sorted(box_with_value, key = lambda x:x[1], reverse = reverse)

    return box_with_value

  def cal_good_composites(self, handCards, otherHands, otherHandNumbers):
    box = []
    current = []

    start3 = time.perf_counter()
    otherHandsGroup = make_hand_group(otherHands)
    self.deep_search5(handCards,current, box)
    end3 = time.perf_counter()
    print(f"time3:{end3-start3:.6f}\n")

    #merge 3+2, 4+1 composites
    start4 = time.perf_counter()
    self.merge_moves_in_each_strategy(box)
    end4 = time.perf_counter()
    print(f"time4:{end4-start4:.6f}\n")

    start5 = time.perf_counter()
    if STRATEGY_TYPE == STRATEGY_TYPE_LEN:
      for i in range(len(box)):
        box[i] = [box[i], len(box[i])]
      box = self.sort_box_by_value(box)
    elif STRATEGY_TYPE == STRATEGY_TYPE_PROBABILITY:
      for i in range(len(box)):
        value = self.cal_strategy_value(box[i], otherHands, otherHandsGroup, otherHandNumbers)
        box[i] = [box[i], value]
      box = self.sort_box_by_value(box, reverse = True)
    elif STRATEGY_TYPE == STRATEGY_TYPE_EXPECTATION:
      for i in range(len(box)):
        value = self.cal_strategy_expectation_length(box[i], otherHands, otherHandsGroup, otherHandNumbers)
        box[i] = [box[i], value]
      box = self.sort_box_by_value(box, reverse = True)
    end5 = time.perf_counter()
    print(f"time5:{end5-start5:.6f}\n")
    # TEST
    # box2 = []
    # for i in range(len(box)):
    #   box2.append([box[i], len(box[i])])
    # box2 = self.sort_box_by_value(box2)
    # for i in range(len(box2)):
    #   box2[i] = box2[i][0]



    #TEST
    # box3 = []
    # for i in range(len(box)):
    #   box3.append(box[i][0])

    return box
    
  def deep_search1(self, handCards, current, box):
    moves = self.cal_one_cards(handCards)
    current += moves

    #filter num_of_4 > num_of_1 current
    num_of_1 = strategy_of_length_n_number(current, 1)
    num_of_4 = strategy_of_length_n_number(current, 4)
    if (num_of_4 <= num_of_1):
      box.append(current)
    return

  def deep_search2(self, handCards, current, box):
    if len(handCards) >= 2:
      moves = self.cal_two_cards(handCards)
      for move in moves:
        #add logic to remove permute roles
        bingo = check_group2_is_greater_or_equal_than_group2(move, current)
        if bingo:
          newCards = sub_cards(handCards, move)
          newCurrent = copy.deepcopy(current)
          newCurrent.append(move)
          self.deep_search2(newCards, newCurrent, box)
      
    self.deep_search1(handCards, current, box)
    return  
      
  def deep_search3(self, handCards, current, box):
    if len(handCards) >= 3:
      moves = self.cal_three_cards(handCards)
      for move in moves:
        bingo = check_group3_is_greater_or_equal_than_group3(move, current)
        if bingo:
          newCards = sub_cards(handCards, move)
          newCurrent = copy.deepcopy(current)
          newCurrent.append(move)
          if len(newCards) == 0:
            #filter num_of_4 > num_of_1 current
            num_of_1 = strategy_of_length_n_number(newCurrent, 1)
            num_of_4 = strategy_of_length_n_number(newCurrent, 4)
            if num_of_4 <= num_of_1:
              box.append(newCurrent)
            return
          self.deep_search3(newCards, newCurrent, box)
      
    self.deep_search2(handCards, current, box)

  def deep_search4(self, handCards, current, box):
    if len(handCards) >= 4:
      moves = self.cal_four_cards(handCards)
      for move in moves:
        bingo = check_group4_is_greater_or_equal_than_group4(move, current)
        if bingo:
          newCards = sub_cards(handCards, move)
          newCurrent = copy.deepcopy(current)
          newCurrent.append(move)
          self.deep_search4(newCards, newCurrent, box)
      
    self.deep_search3(handCards, current, box)
    return 
  
  def deep_search5(self, handCards, current, box):
    if(len(handCards) >=5):
      moves = self.cal_straight_and_flush(handCards)
      for move in moves:
        newCards = sub_cards(handCards, move)
        newCurrent = copy.deepcopy(current)
        newCurrent.append(move)
        self.deep_search5(newCards, newCurrent, box)
      
    self.deep_search4(handCards, current, box)
    return 

  def cal_one_cards(self, handCards):
    output = []
    for card in handCards:
      output.append([card])
    return output

  #calculate all possible two-cards play
  def cal_two_cards(self, handCards):
    handGroup = make_hand_group(handCards)
    return self.cal_two_cards_by_hand_group(handGroup)

  def cal_two_cards_by_hand_group(self, handGroup):
    output = []
    for group in handGroup:
      for i in range(len(group)-1):
        for j in range(i+1, len(group)):
          output.append([group[i],group[j]])
    return output    
  
  def cal_three_cards(self, handCards):
    output = []
    handGroup = make_hand_group(handCards)
    for group in handGroup:
      for i in range(len(group)-2):
        for j in range(i+1, len(group)-1):
          for k in range(j+1, len(group)):
            output.append([group[i],group[j],group[k]])
    return output
  
  def cal_three_cards_by_hand_group(self,handGroup):
    output = []
    for group in handGroup:
      for i in range(len(group)-2):
        for j in range(i+1, len(group)-1):
          for k in range(j+1, len(group)):
            output.append([group[i],group[j],group[k]])
    return output    

  def cal_four_cards(self, handCards):
    output = []
    handGroup = make_hand_group(handCards)
    for group in handGroup:
      if len(group) == 4:
        output.append(group)
    return output

  def cal_straight_and_flush(self, handCards):
    handGroup = make_hand_group(handCards)
    flushGroup = make_flush_group(handCards)
    output = self.cal_flush(flushGroup)
    output2 = self.cal_straight(handGroup)
    return output + output2

  def cal_straight(self, handGroup):
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
                  output.append(playCards)
    return output   
  
  def cal_flush(self, flushGroup):
    output = []
    for i in range(0,len(flushGroup)):
      m = flushGroup[i]
      length = len(m)
      if length <= 9:
        for j1 in range(0,length-4):
          for j2 in range(j1+1,length-3):
            for j3 in range(j2+1,length-2):
              for j4 in range(j3+1,length-1):
                for j5 in range(j4+1,length):
                  output.append([m[j1],m[j2],m[j3],m[j4],m[j5]])
      else:
        print("npc_new__cal_flush_length:%d\n", length)
        for j in range(0, len(flushGroup[i])-4, 1):
          output.append(flushGroup[i][j:j+5])
    return output
  
  def cal_otherHands_numbers(self, myPlayerNum, players):
    output = []
    for i in range(myPlayerNum + 1, len(players)):
      output.append(players[i].handSize)
    for i in range(0, myPlayerNum):
      output.append(players[i].handSize)
    return output

  def sort_by_toBeat_one_value(self, box, toBeat, iter_num):
    
    for i in range(iter_num):
      for j in range(len(box[i][0]) - 1,-1, -1):
        move = box[i][0][j]
        if len(move) == 1:
          re = compare_one(move, toBeat)
          if re == GREATER:
            box[i][-1] = move[0]
            break
          elif re == LESS:
            box[i][-1] = -1
            break

    box[0:iter_num] = self.sort_box_by_value(box[0:iter_num], reverse = True)

    return box
  
  def sort_by_toBeat_two_value(self, box, toBeat, iter_num):
    for i in range(iter_num):
      for j in range(len(box[i][0]) - 1,-1, -1):
        move = box[i][0][j]
        if len(move) == 2:
          re = compare_two(move, toBeat)
          if re == GREATER:
            box[i][-1] = cal_two_value(move)
            break
          elif re == LESS:
            box[i][-1] = -1
            break

    box[0:iter_num] = self.sort_box_by_value(box[0:iter_num], reverse = True)
    return box

  def sort_by_toBeat_three_value(self, box, toBeat, iter_num):
    for i in range(iter_num):
      for j in range(len(box[i][0]) - 1,-1, -1):
        move = box[i][0][j]
        if len(move) == 3:
          re = compare_three(move, toBeat)
          if re == GREATER:
            box[i][-1] = cal_three_value(move)
            break
          elif re == LESS:
            box[i][-1] = -1
            break

    box[0:iter_num] = self.sort_box_by_value(box[0:iter_num], reverse = True)
    return box
  
  def lead_play(self, box, otherHands, otherHandsNumbers, myPlayerNum, minNumCardInOther):
    chosen = choose_from_one_strategy_new(box[0][0], otherHands, otherHandsNumbers, myPlayerNum)
    return chosen
  
  

  def play_card(self, playInfo, myData = ""):  
    myHandCards = playInfo.myHandCards
    otherHands = playInfo.otherHands
    toBeat = playInfo.toBeat
    toBeatId = playInfo.toBeatId
    myPlayerNum = playInfo.myPlayerNum
    leftOvers = playInfo.leftOvers
    first_round_first_play = playInfo.first_round_first_play
    simulate = playInfo.simulate

    playOrder = get_play_order(myPlayerNum, toBeatId)

    lenToBeat = len(toBeat) 

    otherHandsNumbers = leftOvers

    minNumCardinOtherHand = 13
    if simulate == False:
      for i in range(len(leftOvers)):
        minNumCardinOtherHand = min(minNumCardinOtherHand, leftOvers[i])

    start_1 = time.perf_counter()
    box = self.cal_good_composites(myHandCards, otherHands, otherHandsNumbers)
    end_1 = time.perf_counter()
    print(f"time1:{end_1-start_1:.6f} second\n")

   
    if first_round_first_play:
      for i in range(len(box)):
        strategy = box[i][0]
        for s in strategy:
          if CARD_3D in s:
            if len(s) == 5:
              print("card_3d1\n")
              return transform_out(s), str(self.current_folder_time)
            else:
              for g in strategy:
                if len(g) == (5-len(s)):
                  print("card_3d2\n")
                  return transform_out(s+g),str(self.current_folder_time)
            return transform_out(s), str(self.current_folder_time)
    iter_num = min(len(box), BOX_USE_LENGTH)

    chosen = []
    folder = False
    if lenToBeat == 0:
      chosen = choose_from_one_strategy_new(box[0][0], otherHands, otherHandsNumbers, myPlayerNum)

    elif lenToBeat == 1:
      #box =  self.sort_by_toBeat_one_value(box, toBeat, iter_num)
      for i in range(iter_num):
        strategy = box[i][0]
        toPlay, moveType = self.one_card_response_strategy(strategy, toBeat, otherHands, minNumCardinOtherHand, simulate)
        if moveType == PLAY_CARD and len(toPlay) != 0:
          print(f"max_iter_num:{i}\n")
          chosen = toPlay
          break
        elif moveType == FOLDER:
          folder = True
          chosen = []
          break
        else:
          pass
    elif lenToBeat == 2:
      #box =  self.sort_by_toBeat_two_value(box, toBeat, iter_num)
      for i in range(iter_num):
        strategy = box[i][0]
        for s in strategy:
          if len(s) == 2 and GREATER ==  compare_two(s,toBeat):
            chosen = s
            break
        if len(chosen)>0:
          break
    elif lenToBeat ==3:
      #box =  self.sort_by_toBeat_three_value(box, toBeat, iter_num)
      for i in range(iter_num):
        strategy = box[i][0]
        for s in strategy:
          if len(s) == 3 and GREATER ==  compare_three(s,toBeat):
            chosen = s
            break
        if len(chosen)>0:
          break      
    elif lenToBeat == 5:
      for i in range(iter_num):
        strategy = box[i][0]
        for s in strategy:
          if len(s) == 5:
            if GREATER == compare_five(s, toBeat):
              chosen = s
              break
        if len(chosen) >0:
          break           
    else:
      print("Can't beat!\n")
      #raise Exception('lenToBeat:%d!\n',lenToBeat)
    
    if chosen == [] and folder == False:
      print("No Solution!\n")


    if chosen != [] and folder == False and len(toBeat) > 0:
      otherHandGroup = make_hand_group(otherHands)
      #consider strategy folder:
      #there are many conditions here:
      #1. the toBeat is not very small, since that is for me to pass card
      #2. toBeat is big, but previous-play player is also this man, that means I can't wait
      #3. toBeat is big and previous-play player is not him, but his cards number are
      # 1,2,3,5, that means if I don't beat, he could play off all. so I won't
      # now here I should folder 
      if playOrder == PREVIOUS_PLAY:
        if toBeat[-1] >= toNumber('AD'):
          if True: #lastFolder and lastFolderId == 
            if leftOvers[2] not in [1,2,3,5]:
              p = self.probability_of_bigger_pair_not_exist(chosen, otherHandGroup, leftOvers)
              if p >= 0.9:
                print('strategy_folder!\n')
                return [],str(self.current_folder_time)
      elif playOrder == POST_PLAY:
        pass
      else:
        pass

    return transform_out(chosen), str(self.current_folder_time)
  
  def whether_fold_one(self,one_card, minNumCardinOtherHand, otherHands):
    print("whether_fold_one!\n")
    p_max = otherHands[-1]
    if p_max - one_card > 0 and (p_max - one_card) < 4 and minNumCardinOtherHand > 2 :
      return True
    return False 
  
  def one_card_response_strategy(self, strategy, toBeat, otherHands, minNumCardinOtherHand, simulate):
    num_1 = strategy_of_length_n_number(strategy,1)
    if num_1 == 0:
      return [], NOBEAT
    
    moves = select_all_length_n_moves(strategy, 1)
    card = moves[-1][0]
    if card <= toBeat[0]:
      return [], NOBEAT
    
    if num_1 == 1:
      for s in strategy:
        if len(s) == 1:
          if GREATER ==  compare_one(s,toBeat):
            if simulate == False and len(otherHands) > 0:
              fold = self.whether_fold_one(s[0], minNumCardinOtherHand, otherHands)
              if fold == True:
                if self.current_folder_time < MAX_FOLDER_TIME_IN_A_GAME:
                 self.current_folder_time += 1
                 print("folder!\n")
                 return [], FOLDER

    if simulate == False and len(otherHands) > 0:
      diff = card - otherHands[-1]
      if diff > 0:
        if num_1 == 1 or moves[-2][0] < toBeat[0]:
          if minNumCardinOtherHand >= MIN_NUM_CARD_IN_OTHER_HAND_FOR_FOLDER:
            mid_cards = []
            for i in range(toBeat[0] +1, card):
              mid_cards.append(i)
            for mid in mid_cards:
              if mid in otherHands:
                if self.current_folder_time < MAX_FOLDER_TIME_IN_A_GAME:
                  self.current_folder_time += 1
                  print("folder!\n")
                  return [],FOLDER
      else:
        pass
        if diff >=(-4) and minNumCardinOtherHand >= MIN_NUM_CARD_IN_OTHER_HAND_FOR_FOLDER and (num_1 == 1 or moves[-2][0] < toBeat[0]):
          if self.current_folder_time < MAX_FOLDER_TIME_IN_A_GAME:
            self.current_folder_time += 1
            print("folder2!\n")
            return [],FOLDER
          
    for move in moves:
      if move[0] > toBeat[0]:
        return move, PLAY_CARD
    return [], NOBEAT