from classes import *


import copy

#####################helper#########################
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
    if len(cards) == 0:
      if len(handGroup) < 5:
        return []
      else:
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

  




###############################npc-end############


###################algorithm##################
ranks = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']
suits = ['D', 'C', 'H', 'S']

class Algorithm:

    def transform_in(self, myHand):
      output = []
      for i in range(len(myHand)):
          card = myHand[i]
          id = ranks.index(card[0])*4+suits.index(card[1])
          output.append(id)
      output = sorted(output)
      return output
    
    def transform_out(self, cards):
      output = []
      for i in range(len(cards)):
        card = cards[i]
        rank = get_rank(card)
        suit = get_suit(card)
        output.append(f'{ranks[rank]}{suits[suit]}')
      return output
        
    def getAction(self, state: MatchState):
      action = []             # The cards you are playing for this trick
      myData = state.myData   # Communications from the previous iteration

      # TODO Write your algorithm logic here
      myHandCards = self.transform_in(state.myHand)
      if(len(state.matchHistory) == 0):
        print("len(state.matchHistory)==0!\n")
        return action, myData 
      
      gameHistory = state.matchHistory[-1]
      rounds = gameHistory.gameHistory
      played_cards = []
      for i in range(len(rounds)):
        for trick in rounds[i]:
          played_cards += self.transform_in(trick.cards)

      #formulate the state:
      card_state = [IN_OTHER_HAND] * 52
      for card in played_cards:
          card_state[card] = CARD_PLAYED
      for card in myHandCards:
          card_state[card] = IN_MY_HAND
      
      #current
      #table = Table() #time consuming 
      table = None

      card_state0 = [CARD_PLAYED] * 52
      for card in myHandCards:
          card_state0[card] = IN_MY_HAND
      
      toBeat = self.transform_in(state.toBeat.cards)
      
      other_cards = get_other_cards(card_state)
      card_number = len(other_cards)
      if card_number > 13:
        card_number = 13 

      #npc samples:
      npc_samples = []
      for j in range(NPC_LOOP):
        sample_cards = random.sample(other_cards, card_number)
        npc_samples.append(sample_cards)

      #loops for sample a card-play (strategy)
      strategies = []
      max = 0
      ind = 0
      npc = NPC(card_state0, table)
      moves = npc.cal_possible_moves(toBeat)
      times = min(len(moves), SAMPLE_LOOP)
      print(f"possible_moves_num:{times}\n")
      if times == 0:
        return [], myData
      #this loop decide which cards to play
      for i in range(times):
        cards = npc.legal_random(toBeat)
        strategies.append(cards)
        if cards == None:
          #this means can't beat, so only choice is pass
          print("cant't beat\n")
          return [], myData
        
        #loops for create npc
        score_for_all_npc = 0
        #this loop decide which cards given to npc
        for j in range(NPC_LOOP):
          #construct a random npc
          sample_cards = npc_samples[j]
          card_state1 = [CARD_PLAYED] * 52
          for card in sample_cards:
            card_state1[card] = IN_MY_HAND

          #loops for mcts
          total_value = 0
          #this loop is for mcts sampling
          for k in range(MCTS_LOOP):
            win = NPC0_WIN
            step = 0

            npc0 = NPC(card_state0, table)
            npc1 = NPC(card_state1, table)
            new_cards = copy.deepcopy(cards)
            for l in range(TREE_SEARCH):
              new_cards = npc1.play_random(new_cards)
              if new_cards == None or len(new_cards) == 0:
                win = NPC0_WIN
                step = l
                break

              new_cards = npc0.play_random(new_cards)
              if new_cards == None or len(new_cards) == 0:
                win = NPC1_WIN
                step = l
                break
              step += 1
        
            value = calculate_value(step, win)
            total_value += value 
          
          score_for_all_npc += total_value

        if score_for_all_npc > max:
          max= score_for_all_npc
          ind = i
        
      final_move = strategies[ind]
      action = self.transform_out(final_move)


      return action, myData