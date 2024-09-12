import random 


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
STRAIGHT = 0 #顺子
FLUSH = 1 #同花
FOUR_OF_A_KIND = 2 #炸
FULL_HOUSE = 3 #3带2
STRAIGHT_FLUSH = 4 #同花顺

NPC0_WIN = 0
NPC1_WIN = 1

NPC_LOOP = 5
SAMPLE_LOOP = 10
MCTS_LOOP = 10 
TREE_SEARCH = 10



def create_ordered_cards():
  cards = [0] * 52
  for i in range(0,52):
    cards[i] = i
  return cards 

def create_shuffled_cards():
  cards = create_ordered_cards()
  random.shuffle(cards)
  return cards

def get_rank(a):
  return a//4

def get_suit(a):
  return a%4

def compare5_straight(left, right):
  return left[4] < right[4]

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
  if right[2]//4 == right[2]//4:
    r = right[2]
  else:
    r = right[4]
  if get_rank(l) < get_rank(r):
    return True
  elif get_rank(l) > get_rank(r):
    return False
  
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


def card5_type(sorted_cards):
  card_type = NOTHING
  ranks = [get_rank(card) for card in sorted_cards]
  if ranks[1] == ranks[0]+1 and ranks[2] == ranks[1]+1:
    card_type = STRAIGHT
    suits = [get_suit(card) for card in sorted_cards]
    if suits[0]==suits[1] and suits[0] == suits[2] and suits[0]==suits[3] and suits[0] == suits[4]:
      card_type = STRAIGHT_FLUSH
    return card_type
  
  if (ranks[0]==ranks[1] and ranks[0]==ranks[2] and ranks[0]==ranks[3]) or (ranks[1]==ranks[2] and ranks[2]== ranks[3] and ranks[3]==ranks[4]):
    card_type = FOUR_OF_A_KIND
    return card_type
  
  if((ranks[0] == ranks[1] and ranks[0] == ranks[2] and ranks[3]== ranks[4]) or (ranks[0]==ranks[1] and ranks[2]==ranks[3] and ranks[3] == ranks[4])):
    card_type == FULL_HOUSE
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

  value += times * 10
  return value

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


  