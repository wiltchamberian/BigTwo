from classes import *

VERSION = "2.18.25_add_numeric_sort"

import copy
from functools import cmp_to_key
#####################helper#########################
import random 
import time


STRATEGY_TYPE_LEN = 0
STRATEGY_TYPE_PROBABILITY = 1
STRATEGY_TYPE_EXPECTATION = 2
STRATEGY_TYPE_OPTIMIZED_LEN = 3
STRATEGY_TYPE_COMPARE = 4 #compare each other


#choose strategy
STRATEGY_TYPE = STRATEGY_TYPE_EXPECTATION
MAX_FOLDER_TIME_IN_A_GAME = 5
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

NO_PLAY = 3
PREVIOUS_PLAY = 2
POST_PLAY = 0
MIDDLE_PLAY = 1

ranks = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']
suits = ['D', 'C', 'H', 'S']

def complement(hands):
  all = [0]*52
  for hand in hands:
    all[hand]=1
  output = []
  for i in range(52):
    if all[i]==0:
      output.append(all[i])
  return output
  
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
  elif (toBeatId+2)%4 == myId:
    return MIDDLE_PLAY

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
  sg = sorted(strategy, key = cmp_to_key(strategy_compare))
  return sg

def distrib_compare(box1, box2):
  dis1 = box1[1]
  dis2 = box2[1]

  if dis1[1] < dis2[1]:
    return LESS 
  elif dis1[1] > dis2[1]:
    return GREATER
  
  if dis1[2] < dis2[2]:
    return LESS
  elif dis1[2] > dis2[2]:
    return GREATER 
  
  if dis1[3] < dis2[3]:
    return LESS
  elif dis1[3] > dis2[3]:
    return GREATER

  if dis1[5] <dis2[5]:
    return LESS 
  elif dis1[5]> dis2[5]:
    return GREATER

  return EQUAL

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

def cal_three_value(a):
  return get_rank(a[0])

def cal_five_value(a):
  return 5.0

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
  rank1 = get_rank(a1[-1])
  rank2 = get_rank(a2[-1])
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

def get_prob_from_type5(tp):
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
  else:
    return 1.0

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

def get_one_cards_order_fraction(cards, otherHands):
  card = cards[0]
  if card < otherHands[0]:
    return 0.0
  elif card > otherHands[-1]:
    return 1.0
  for i in range(len(otherHands)):
    if card < otherHands[i]:
      return float(i)/float(len(otherHands))
  return 0.0

def get_one_cards_ranking(cards, otherHands):
  n = 0
  for i in range(len(otherHands)-1,-1,-1):
    if cards[0] > otherHands[i]:
      return n
    n += 1
  return n

def choose_from_one_strategy_new(strategy, other_hands, leftOvers, myPlayerId):
  npc = NewNPC()

  otherHandGroup = make_hand_group(other_hands)

  sg = sort_strategy(strategy)
  move_count = len(sg)

  splits = split_moves_according_to_length(sg)

  
  moveLengths = cal_move_length_in_strategy(sg)
  
  move_count = len(sg)

  minNumCardInOtherHand = cal_min_num_cards(leftOvers)

  total_play_number = len(splits[1])+len(splits[2])+len(splits[3])+len(splits[5])
  residue_play_number = total_play_number
  total_series_number = 0
  for split in splits:
    if len(split)>0:
      total_series_number += 1

  exp1 = 0.0
  exp2 = 0.0
  exp3 = 0.0
  exp5 = float(len(splits[5]))*5.0

  #if there exist must winner card, play this!
  # all the one cards are a series, all two cards, etc...
  must_win_series_number = 0
  one_series_must_win = False
  two_series_must_win = False
  three_series_must_win = False

  ready_to_play_numCards = 0
  if len(splits[1]) > 0:
    exp1 = npc.cal_one_cards_expectation_length([], splits[1], other_hands, otherHandGroup, leftOvers)
    if exp1 >= (float(len(splits[1]))-0.00001):
      must_win_series_number += 1
      residue_play_number -= len(splits[1])
      one_series_must_win = True

      if residue_play_number == 1:
        return splits[1][0]

  if len(splits[2]) > 0:
    exp2 = npc.cal_two_cards_expectation_length([], splits[2], other_hands, otherHandGroup, leftOvers)
    if exp2 >= (float(2*len(splits[2]))-0.00001):
      must_win_series_number += 1
      residue_play_number -= len(splits[2])
      two_series_must_win = True

      if residue_play_number == 1:
        return splits[2][0]
      
  if len(splits[3]) > 0:
    exp3 = npc.cal_three_cards_expectation_length([], splits[3], other_hands, otherHandGroup, leftOvers)
    if exp3 >= (float(3*len(splits[3]))-0.00001):
      must_win_series_number +=1 
      three_series_must_win = True
      residue_play_number -= len(splits[3])
      if residue_play_number == 1:
        return splits[3][0]
  
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
  #the reason is if I play small single first, I have a chance to play the bigger single, but it would be beat, then no chance to play five.
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
    if q2 < q1:
      return splits[1][0]
    
    if len(splits[2])==1 and len(splits[1])>=4:
      if q2 < 0.9:
        return splits[1][0]
      else:
        # this shows the singles are not bigger enough but pairs are big, play single
        if splits[2][0][0] > splits[1][-1][0]:
          return splits[1][0]

    return splits[2][0]

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

  #only fives
  if moveLengths[5]>0 and moveLengths[1]==0 and moveLengths[2] == 0 and moveLengths[3] == 0:
    #play bigger five first
    return splits[5][-1]
    

  mm = max(exp1,exp2,exp3,exp5)
  if len(splits[1])> 0 and mm == exp1:
    return splits[1][0]
  if len(splits[2])> 0 and mm == exp2:
    return splits[2][0]
  if len(splits[3])> 0 and mm == exp3:
    return splits[3][0]
  if len(splits[5])> 0 and mm == exp5:
    return splits[5][0]


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


###########################simulate########################
def simulate_one_card_play_one_round(toBeat, myHands, hands1, hands2, hands3):
  low = toBeat
  numPlayedCards = 0
  while True:
    ps = 0
    play = None
    for i in range(len(myHands)):
      if low < myHands[i]:
        play = myHands[i]
        low = myHands[i]
        del myHands[i]
        numPlayedCards += 1
        break
    if play == None:
      break
    elif len(myHands) == 0:
      break

    play = None
    for i in range(len(hands1)):
      if low < hands1[i]:
        play = hands1[i]
        low = hands1[i]
        del hands1[i]
        break
    if play== None:
      ps += 1
    elif len(hands1) == 0:
        break

    play = None
    for i in range(len(hands2)):
      if low < hands2[i]:
        play = hands2[i]
        low = hands2[i]
        del hands2[i]
        break
    if play== None:
      ps += 1
    elif len(hands2) == 0:
      break

    play = None
    for i in range(len(hands3)):
      if low < hands3[i]:
        play = hands3[i]
        low = hands3[i]
        del hands3[i]
        break
    if play== None:
      ps += 1
    elif len(hands3) == 0:
      break

    if ps == 3:
      low = -1

  return numPlayedCards


def simulate_one_card_play_expectation(toBeat, myCards, otherHands, leftOvers):
  seed_value = int(time.time())
  random.seed(seed_value)
  others = copy.deepcopy(otherHands)
  expl = 0.0
  for i in range(MCTS_LOOP):
    random.shuffle(others)
    hands1 = others[0:leftOvers[0]]
    hands1 = sorted(hands1)
    hands2 = others[leftOvers[0]:leftOvers[0]+leftOvers[1]]
    hands2 = sorted(hands2)
    hands3 = others[leftOvers[0]+leftOvers[1]: leftOvers[0]+leftOvers[1]+leftOvers[2]]
    hands3 = sorted(hands3)
    myHands = copy.deepcopy(myCards)
    numPlayedCards = simulate_one_card_play_one_round(toBeat,myHands,hands1,hands2, hands3)
    expl += numPlayedCards
  expl = expl/MCTS_LOOP

  return expl


def simulate_two_cards_play_one_round(toBeat, myHands, hands1, hands2, hands3):
  low = toBeat
  numPlayedCards = 0
  handsGroup = [hands1,hands2,hands3]
  while True:
    ps = 0
    play = None
    for i in range(len(myHands)):
      if compare_two(low, myHands[i])== LESS:   
        play = myHands[i]
        low = myHands[i]
        del myHands[i]
        numPlayedCards += 2
        break
    if play == None:
      break
    elif len(myHands) == 0:
      break

    for hands in handsGroup:
      play = None
      for i in range(len(hands)):
        if (len(hands[i]) == 2 and LESS==compare_two(low,hands[i])) or (len(hands[i])==3 and LESS==compare_two(low,hands[i][-2:])):
          play = hands[i][-2:]
          low = hands[i][-2:]
          del hands[i]
          break
        elif len(hands[i]) == 4 and LESS==compare_two(low, hands[i][-2:]):
          play = [hands[i][0],hands[i][3]]
          low = [hands[i][0],hands[i][3]]
          hands[i] = [hands[i][1],hands[i][2]]
          break
      if play== None:
        ps += 1
      elif len(hands) == 0:
          break
    if len(hands1) == 0 or len(hands2) == 0 or len(hands3) == 0:
      break

    if ps == 3:
      low = [-1,-1]

  return numPlayedCards


def simulate_two_cards_play_expectation(toBeat, split, otherHands, leftOvers):
  seed_value = int(time.time())
  random.seed(seed_value)
  others = copy.deepcopy(otherHands)
  expl = 0.0
  for i in range(MCTS_LOOP):
    random.shuffle(others)
    hands1 = others[0:leftOvers[0]]
    hands1 = sorted(hands1)
    hands1 = make_hand_group(hands1)
    hands1 = [sub_array for sub_array in hands1 if len(sub_array)>1 ]
    hands2 = others[leftOvers[0]:leftOvers[0]+leftOvers[1]]
    hands2 = sorted(hands2)
    hands2 = make_hand_group(hands2)
    hands2 = [sub_array for sub_array in hands2 if len(sub_array)>1 ]
    hands3 = others[leftOvers[0]+leftOvers[1]: leftOvers[0]+leftOvers[1]+leftOvers[2]]
    hands3 = sorted(hands3)
    hands3 = make_hand_group(hands3)
    hands3 = [sub_array for sub_array in hands3 if len(sub_array)>1 ]
    myHands = copy.deepcopy(split)
    numPlayedCards = simulate_two_cards_play_one_round(toBeat,myHands,hands1,hands2, hands3)
    expl += numPlayedCards
  expl = expl/MCTS_LOOP

  return expl


def simulate_three_cards_play_one_round(toBeat, myHands, hands1, hands2, hands3):
  low = toBeat
  numPlayedCards = 0
  handsGroup = [hands1,hands2,hands3]
  while True:
    ps = 0
    play = None
    for i in range(len(myHands)):
      if compare_three(low, myHands[i])== LESS:   
        play = myHands[i]
        low = myHands[i]
        del myHands[i]
        numPlayedCards += 3
        break
    if play == None:
      break
    elif len(myHands) == 0:
      break

    for hands in handsGroup:
      play = None
      for i in range(len(hands)):
        if len(hands[i]) == 3 and LESS == compare_three(low,hands[i]):
          play = hands[i]
          low = hands[i]
          del hands[i]
          break
        elif len(hands[i]) == 4 and LESS == compare_three(low, hands[i][0:3]):
          play = hands[i][0:3]
          low = hands[i][0:3]
          del hands[i]
          break
      if play == None:
        ps += 1
      elif len(hands) == 0:
          break
    if len(hands1) == 0 or len(hands2) == 0 or len(hands3) == 0:
      break

    if ps == 3:
      low = [-1,-1,-1]

  return numPlayedCards

def simulate_three_cards_play_expectation(toBeat, split, otherHands, leftOvers):
  seed_value = int(time.time())
  random.seed(seed_value)
  others = copy.deepcopy(otherHands)
  expl = 0.0
  for i in range(MCTS_LOOP):
    random.shuffle(others)
    hands1 = others[0:leftOvers[0]]
    hands1 = sorted(hands1)
    hands1 = make_hand_group(hands1)
    hands1 = [sub_array for sub_array in hands1 if len(sub_array)>2 ]
    hands2 = others[leftOvers[0]:leftOvers[0]+leftOvers[1]]
    hands2 = sorted(hands2)
    hands2 = make_hand_group(hands2)
    hands2 = [sub_array for sub_array in hands2 if len(sub_array)>2 ]
    hands3 = others[leftOvers[0]+leftOvers[1]: leftOvers[0]+leftOvers[1]+leftOvers[2]]
    hands3 = sorted(hands3)
    hands3 = make_hand_group(hands3)
    hands3 = [sub_array for sub_array in hands3 if len(sub_array)>2 ]
    myHands = copy.deepcopy(split)
    numPlayedCards = simulate_three_cards_play_one_round(toBeat,myHands,hands1,hands2, hands3)
    expl += numPlayedCards
  expl = expl/MCTS_LOOP

  return expl

###########################simulate-end######################

#############################npc#####################

#Monte Carlo tree search



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


      print(f"{VERSION}\n")
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
    return get_prob_from_type5(tp)
    
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
  
  def cal_one_cards_expectation_length_old(self, split, otherHands):
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

  def cal_one_cards_expectation_length(self, toBeat, split, otherHands, otherHandsGroup, leftOvers):
    if len(split) == 0 or len(otherHands) == 0:
      return 0.0 

    expl = 0.0
    for i in range(len(split)//2, len(split)):
      p = self.probability_of_bigger_one_not_exist(split[i], otherHands, leftOvers)
      expl += 2.0 * p
    # fracs = []
    # for i in range(len(split)//2, len(split)):
    #   if split[i][0] > otherHands[-1]:
    #     fracs.append(1.0)
    #     continue
    #   for j in range(len(otherHands)):
    #     if split[i][0] < otherHands[j]:
    #       fracs.append(float(j)/len(otherHands))
    #       break

    # expl = 0.0
    # if len(split)%2 == 0:
    #   for i in range(len(fracs)-1, -1, -1):
    #     #if fracs[i] >= 0.95:
    #     expl += 2.0 * fracs[i]
    # else:
    #   for i in range(len(fracs)-1, 0,-1):
    #     expl += 2.0 * fracs[i]
    #   expl += 1.0 * fracs[0]

    if expl > len(split):
      expl = len(split)
    
    return expl
  
  def cal_one_cards_expectation_length_mcts(self, toBeat, split, otherHands, otherHandsGroup, leftOvers):
    if len(split) == 0 or len(otherHands) == 0:
      return 0.0 

    myCards = [card[0] for card in split]
    myCards = sorted(myCards)

    expl = simulate_one_card_play_expectation(toBeat[0], myCards, otherHands, leftOvers )
    return expl
  
  def cal_two_cards_expectation_length_mcts(self, toBeat, split, otherHands, otherHandsGroup, leftOvers):
    if len(split) == 0 or len(otherHands) == 0:
      return 0.0 
    
    expl = simulate_two_cards_play_expectation(toBeat, split, otherHands, leftOvers)
    return expl

  def cal_three_cards_expectation_length_mcts(self, toBeat, split, otherHands, otherHandsGroup, leftOvers):
    if len(split) == 0 or len(otherHands) == 0:
      return 0.0 
    
    expl = simulate_three_cards_play_expectation(toBeat, split, otherHands, leftOvers)
    return expl
  
  #a very extremly formula, to be optimized (FIX ME)
  def cal_two_cards_expectation_length_old(self, split, otherHands, otherHandsGroup, leftOvers):
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
  
  def cal_two_cards_expectation_length(self, toBeat, split, otherHands, otherHandsGroup, leftOvers):
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

    pairs = sorted(pairs, key = cmp_to_key(compare_two))

    if len(pairs) == 0:
      return float(len(split)) * 2.0

    ###
    expl = 0.0
    for i in range(len(split)//2, len(split)):
      p = self.probability_of_bigger_pair_not_exist(split[i], otherHandsGroup, leftOvers)
      expl += 4.0 * p

    
    # fracs = []
    # for i in range(len(split)//2, len(split)):
    #   if compare_two(split[i],pairs[-1])==GREATER:
    #     fracs.append(1.0)
    #     continue
    #   for j in range(len(pairs)):
    #     if compare_two(split[i], pairs[j]) == LESS:
    #       fracs.append(float(j)/len(pairs))
    #       break
        
    
    # expl = 0.0
    # if len(split)%2 == 0:
    #   for i in range(len(fracs)-1, -1, -1):
    #     expl += 4.0 * fracs[i]
    # else:
    #   for i in range(len(fracs)-1, 0,-1):
    #     expl += 4.0 * fracs[i]
    #   expl += 2.0 * fracs[0]

    if expl > float(len(split)) * 2.0:
      expl = float(len(split)) * 2.0
    
    return expl

  def cal_three_cards_expectation_length_old(self, split, otherHands, otherHandsGroup, leftOvers):
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

    if len(threes) == 0:
      return float(len(split)) * 3.0
  

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
  
  def cal_three_cards_expectation_length(self, toBeat, split, otherHands, otherHandsGroup, leftOvers):
    if len(split) == 0 or len(otherHands) == 0:
      return 0.0 

    #now we do sorting
    threes = []
    for i in range(len(otherHandsGroup)):
      if len(otherHandsGroup[i]) == 3:
        threes.append(otherHandsGroup[i])
      elif len(otherHandsGroup[i]) == 4:
        threes.append(otherHandsGroup[i][2:4])

    threes = sorted(threes, key = cmp_to_key(compare_three))

    if len(threes) == 0:
      return float(len(split)) * 3.0
    
    expl = 0.0
    for i in range(len(split)//2, len(split)):
      p = self.probability_of_bigger_three_not_exist(split[i], otherHandsGroup, leftOvers)
      expl += 6.0 * p

    # fracs = []
    # for i in range(len(split)//2, len(split)):
    #   if compare_three(split[i],threes[-1])==GREATER:
    #     fracs.append(1.0)
    #     continue
    #   for j in range(len(threes)):
    #     if compare_three(split[i], threes[j]) == LESS:
    #       fracs.append(float(j)/len(threes))
    #       break
        
    
    # expl = 0.0
    # if len(split)%2 == 0:
    #   for i in range(len(fracs)-1, -1, -1):
    #     expl += 6.0 * fracs[i]
    # else:
    #   for i in range(len(fracs)-1, 0,-1):
    #     expl += 6.0 * fracs[i]
    #   expl += 3.0 * fracs[0]

    if expl > float(len(split)) * 3.0:
      expl = float(len(split)) * 3.0
    
    return expl
  
  def cal_strategy_expectation_length(self, toBeat, strategy, otherHands, otherHandsGroup, leftOvers):
    splits = split_moves_according_to_length(strategy)
    expl = 0.0

    to_beat1 = [-1]
    to_beat2 = [-1,-1]
    to_beat3 = [-1,-1,-1]
    to_beat5 = [-1,-1,-1,-1,-1]
    if len(toBeat) == 1:
      to_beat1 = toBeat
    elif len(toBeat) == 2:
      to_beat2 = toBeat
    elif len(toBeat) == 3:
      to_beat3 = toBeat
    elif len(toBeat) == 5:
      to_beat5 = toBeat

    exp1 = 0.0
    exp2 = 0.0
    exp3 = 0.0
    exp5 = 0.0
    if len(splits[1]) > 0:
      exp1 += self.cal_one_cards_expectation_length(to_beat1, splits[1], otherHands, otherHandsGroup,leftOvers)
    if len(splits[2]) > 0:
      exp2 += self.cal_two_cards_expectation_length(to_beat2, splits[2], otherHands, otherHandsGroup,leftOvers )
    if len(splits[3]) > 0:
      exp3 += self.cal_three_cards_expectation_length(to_beat3, splits[3], otherHands, otherHandsGroup, leftOvers)
    if len(splits[5])>0:
      # for move in splits[5]:
      #   tp = card5_type(move)
      #   pb = get_prob_from_type5(tp)
      #   exp5 += 5.0 * pb
      exp5 += 5.0 * len(splits[5]) #FIXME

    expl = exp1 + exp2 + exp3 + exp5
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
  
  def play_left_first(self, box1, box2):
    hg1 = make_hand_group(box1)
    hg2 = make_hand_group(box2)


    return 
  
  def play_with_each_other(self, box1, box2):
    l = 0
    r = 0
    l = self.play_left_first(box1, box2)
    r = self.play_left_first(box2, box1)


    return l,r

  def cal_strategy_optimized_len(self, strategy, otherHands, otherHandsGroup, leftOvers):
    originalLen = len(strategy)
    splits = split_moves_according_to_length(strategy)
    if len(splits[2])==1 and len(splits[1])> 0:
      p = self.probability_of_bigger_pair_not_exist(splits[2][-1])
      if p >= 0.9:
        pass
      
      
    return 
  

  def cal_good_composites(self, toBeat, handCards, otherHands, otherHandNumbers):
    start_1 = time.perf_counter()

    box = []
    current = []

    # start3 = time.perf_counter()
    otherHandsGroup = make_hand_group(otherHands)
    self.deep_search5(handCards,current, box)
    # end3 = time.perf_counter()
    # print(f"time3:{end3-start3:.6f}\n")

    #merge 3+2, 4+1 composites
    # start4 = time.perf_counter()
    self.merge_moves_in_each_strategy(box)
    # end4 = time.perf_counter()
    # print(f"time4:{end4-start4:.6f}\n")

    start5 = time.perf_counter()
    real_length = min(len(box), BOX_USE_LENGTH)
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
        box[i] = [box[i], len(box[i])]
      box = self.sort_box_by_value(box)
      for i in range(real_length):
        value = self.cal_strategy_expectation_length(toBeat, box[i][0], otherHands, otherHandsGroup, otherHandNumbers)
        box[i][1] = value
      box[0: real_length] = self.sort_box_by_value(box[0: real_length], reverse = True) 
    elif STRATEGY_TYPE == STRATEGY_TYPE_OPTIMIZED_LEN:
      for i in range(len(box)):
        value = self.cal_strategy_optimized_len(box[i], otherHands, otherHandsGroup, otherHandNumbers)
        box[i] = [box[i], value]
      box = self.sort_box_by_value(box)
    elif STRATEGY_TYPE == STRATEGY_TYPE_COMPARE:
      for i in range(len(box)):
        box[i] = [box[i], len(box[i])]
      box = self.sort_box_by_value(box)
      length = min(len(box), BOX_USE_LENGTH)
      winBoard = [0] * length
      for i in range(length):
        for j in range(i+1, length):
          l_win, r_win = self.play_with_each_other(box[i][0],box[j][0])
          winBoard[i] += l_win
          winBoard[j] += r_win
      for i in range(length):
        box[i][1] = winBoard[i]
      box = self.sort_box_by_value(box, reverse = True)
    else:
      pass

    # end5 = time.perf_counter()
    # print(f"time5:{end5-start5:.6f}\n")

    end_1 = time.perf_counter()
    print(f"cal_good_composites:{end_1-start_1:.6f} second\n")

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
  
  
  def beat_one_folder(self, myHandCards, myHandGroup,strategy, toBeat, otherHands, leftOvers):
    splits = split_moves_according_to_length(strategy)
    #only a single + a pair and single can't beat toBeat
    if len(splits[1]) ==1 and len(splits[2])==1 and len(splits[3]) == 0 and len(splits[5]) == 0:
      if splits[1][0][-1] < toBeat[0]:
        if splits[2][0][-1] < otherHands[-1] and leftOvers[0]>3 and leftOvers[1]>3 and leftOvers[2]>3:
          return True
    return False

  def two_cards_folder(self, s, strategy, otherHands, leftOvers):
    isFolder = False
    p = self.probability_of_bigger_one_not_exist([s[1]], otherHands, leftOvers)
    if p > 0.99:
      isFolder = True
    if s[1] > toNumber('2D'):
      isFolder = True
    
    mi = min(min(leftOvers[0],leftOvers[1]),leftOvers[2])
    if mi == 2:
      isFolder = False
    return isFolder

  def three_cards_folder(self, s, strategy, otherHands, leftOvers):
    isFolder = False
    p = self.probability_of_bigger_one_not_exist([s[2]], otherHands, leftOvers)
    if p > 0.99:
      isFolder = True
    if s[2] > toNumber('2C'):
      isFolder = True
    
    mi = min(min(leftOvers[0],leftOvers[1]),leftOvers[2])
    if mi == 3:
      isFolder = False
    return isFolder


  def cal_numeric_value_distrib(self, strategy):
    distrib = [0,0,0,0,0,0]
    splits = split_moves_according_to_length(strategy)
    
    #cal later half value
    s1 =  len(splits[1])//2
    d1 =  len(splits[1]) - s1
    for i in range(s1, len(splits[1])):
      distrib[1] += splits[1][i][0]
    if(d1 > 0):
      distrib[1] = float(distrib[1])/d1
    else:
      distrib[1] = 10000

    s2 =  len(splits[2])//2
    d2 =  len(splits[2]) - s2
    for i in range(s2, len(splits[2])):
      distrib[2] += cal_two_value(splits[2][i])
    if d2 > 0:
      distrib[2] = float(distrib[2])/d2
    else:
      distrib[2] = 10000

    s3 = len(splits[3])//2
    d3 = len(splits[3]) - s3
    for i in range(s3, len(splits[3])):
      distrib[3] += cal_three_value(splits[3][i])
    if d3 > 0:
      distrib[3] = float(distrib[3])/d3
    else:
      distrib[3] = 10000

    s5 = len(splits[5])//2
    d5 = len(splits[5]) - s5
    for i in range(s5, len(splits[5])):
      distrib[5] += cal_five_value(splits[5][i])
    if d5>0:
      distrib[5] = float(distrib[5])/d5
    else:
      distrib[5] = 10000
      
    return distrib
  
  def play_card(self, playInfo, myData = ""):  
    myHandCards = playInfo.myHandCards
    otherHands = playInfo.otherHands
    toBeat = playInfo.toBeat
    toBeatId = playInfo.toBeatId
    myPlayerNum = playInfo.myPlayerNum
    leftOvers = playInfo.leftOvers
    first_round_first_play = playInfo.first_round_first_play
    simulate = playInfo.simulate

    myHandGroup = make_hand_group(myHandCards)
    myHandSplits = split_moves_according_to_length(myHandGroup)

    playOrder = get_play_order(myPlayerNum, toBeatId)
    toBeatOrder = playOrder

    lenToBeat = len(toBeat) 

    otherHandsNumbers = leftOvers

    minNumCardinOtherHand = 13
    if simulate == False:
      for i in range(len(leftOvers)):
        minNumCardinOtherHand = min(minNumCardinOtherHand, leftOvers[i])

    box = self.cal_good_composites([], myHandCards, otherHands, otherHandsNumbers)
    iter_num = min(len(box), BOX_USE_LENGTH)

    #tackle ties, if has same mark, bigger singles would be prefered
    v1 = box[0][1]
    split_index = iter_num
    for i in range(iter_num):
      if box[i][1] < v1:
        split_index = i
        break

    for i in range(split_index):
      distrib  = self.cal_numeric_value_distrib(box[i][0])
      box[i][1] = distrib 
    box[0:split_index] = sorted(box[0:split_index], key = cmp_to_key(distrib_compare), reverse = True)

    #recover value
    for i in range(split_index):
      box[i][1] = v1


    
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
    

    chosen = []
    folder = False
    looking_strategy = []
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
          looking_strategy = strategy
          break
        elif moveType == FOLDER:
          folder = True
          chosen = toPlay
          looking_strategy = strategy
          break
        else:
          folder = self.beat_one_folder(myHandCards, myHandGroup, strategy, toBeat, otherHands, leftOvers)
          if folder == True:
            chosen = []
            looking_strategy = strategy
            break


    elif lenToBeat == 2:
      #box =  self.sort_by_toBeat_two_value(box, toBeat, iter_num)
      for i in range(iter_num):
        strategy = box[i][0]
        for s in strategy:
          if len(s) == 2 and GREATER ==  compare_two(s,toBeat):
            #in case of the s is very big and other cards not much, we'll folder
            folder = self.two_cards_folder(s, strategy, otherHands, otherHandsNumbers)
            if folder == True:
              print("two_cards_folder!\n")
              #chosen = []
              break
            chosen = s
            break
        if folder == True or len(chosen) > 0:
          looking_strategy = strategy
          break
    elif lenToBeat ==3:
      #box =  self.sort_by_toBeat_three_value(box, toBeat, iter_num)
      for i in range(iter_num):
        strategy = box[i][0]
        for s in strategy:
          if len(s) == 3 and GREATER ==  compare_three(s,toBeat):
            folder = self.three_cards_folder(s, strategy, otherHands, otherHandsNumbers)
            if folder == True:
              print("three_cards_folder!\n")
              chosen = []
              break
            chosen = s
            break
        if folder == True:
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

    #strategy not folder(special case)
    if len(toBeat) == 1 and folder == True and len(chosen) != 0 and len(looking_strategy)>0:
      #if leftOvers[toBeatOrder] in [1,2,3,5]:
        #print("strategy_not_folder!\n")
        #return transform_out(chosen), str(self.current_folder_time)
      if leftOvers[toBeatOrder] in [10]:
        splits = split_moves_according_to_length(looking_strategy)
        if len(splits[5]) == 0 or card5_type(splits[5][-1])<= FLUSH:
           b1 = (len(splits[2]) > 0 and splits[2][-1][0] >= toNumber('AD'))
           b2 = (len(splits[3])) > 0 and splits[3][-1][0] >= toNumber('AD')
           if b1 or b2:
            print("strategy_not_folder2!\n")
            return transform_out(chosen), str(self.current_folder_time)

    #strategy not folder, in case the toBeatPlayer could play off all his cards:
    if folder == True and len(chosen) != 0:
      if leftOvers[toBeatOrder] in [1,2,3,5]:
        print("strategy_not_folder3!\n")
        return transform_out(chosen), str(self.current_folder_time)


    #strategy folder
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
        if len(toBeat)==1 and toBeat[-1] >= toNumber('AD'):
          if True: #lastFolder and lastFolderId == 
            if leftOvers[2] not in [1,2,3,5]:
              p = self.probability_of_bigger_one_not_exist(chosen, otherHands, leftOvers)
              if p <= 0.9 and leftOvers[0] != len(toBeat) and leftOvers[1] != len(toBeat):
                print('strategy_folder1!\n')
                return [],str(self.current_folder_time)
        if len(toBeat) == 2:
          splits = split_moves_according_to_length(looking_strategy)
          p = self.probability_of_bigger_pair_not_exist(toBeat, otherHandGroup, leftOvers)
          #in this case, the chose pair is my largest pair, only consider folder in this case
          if chosen == splits[2][-1]:
            #in case the previous guy win the game
            if leftOvers[2] not in [1,2,3,5]:
              #in case other guy win the game
              if (leftOvers[0] != len(toBeat) and leftOvers[1] != len(toBeat)) or (p>=0.999):
                #if other people probably have pairs bigger than my choice:
                #that means my pair is not big enough, than I should play but it stll depends
                
                #if my double is small it seems there is no point to folder:
                p_me = self.probability_of_bigger_pair_not_exist(chosen, otherHandGroup, leftOvers)
                if p_me < 0.9:
                  if chosen[-1] >= toNumber('AD'):
                    print('strategy_folder2!\n')
                    return [],str(self.current_folder_time)
                else:
                  print('strategy_folder2!\n')
                  return [],str(self.current_folder_time)
      elif playOrder == POST_PLAY:
        pass
      else:
        pass

    if folder == True:
      return [], str(self.current_folder_time)
    return transform_out(chosen), str(self.current_folder_time)
  
  def whether_fold_one(self, strategy, one_card_moves, just_beat_card, max_single_card, minNumCardinOtherHand, otherHands):
    if just_beat_card < max_single_card:
      #in this case normally don't folder
      return False
    
    #in this case there is bigger single card greater than my card so I folder
    p_max = otherHands[-1]
    rk = get_one_cards_ranking([max_single_card], otherHands)
    if p_max - max_single_card > 0 and rk <= 4 and minNumCardinOtherHand > 2 :
      print("whether_folder1\n")
      return True
    
    #in this case there is no bigger single card greater than my card,
    #but my second biggest single card is large and not large enough, consider folder
    if len(one_card_moves)>=2:
      rk2 = get_one_cards_ranking(one_card_moves[-2], otherHands)
      if p_max - one_card_moves[-2][0] > 0 and rk2 <= 3 and minNumCardinOtherHand > 2:
        print("whether_folder2\n")
        return True

    return False 
  
  def one_card_response_strategy(self, strategy, toBeat, otherHands, minNumCardinOtherHand, simulate):    
    moves = select_all_length_n_moves(strategy, 1)
    if len(moves) == 0:
      return [], NOBEAT
    
    max_single_card = moves[-1][0]
    if max_single_card <= toBeat[0]:
      return [], NOBEAT
    
    if minNumCardinOtherHand == 1:
      #play from big to small
      print("play big to small1!")
      return moves[-1],PLAY_CARD

    just_beat_card = max_single_card
    for move in moves:
      if move[0] > toBeat[0]:
        just_beat_card = move[0]
        break
     
    fold = self.whether_fold_one(strategy, moves, just_beat_card, max_single_card, minNumCardinOtherHand, otherHands)
    if fold == True:
      if self.current_folder_time < MAX_FOLDER_TIME_IN_A_GAME:
        self.current_folder_time += 1
        print("folder!\n")
        return [just_beat_card], FOLDER
    
    for move in moves:
      if move[0] > toBeat[0]:
        return move, PLAY_CARD
    return [], NOBEAT