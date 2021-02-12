import sys
from collections import Counter


# class HandStrength:

	# def __init__(self, img_path):
	# 	self.img_path = img_path

#Use hand_value_check function with argument of the format:
#('5d', 'Qd'), 'Ad', 'Kd', 'Jd', 'Td'

hand_values = {
		"Straight flush": [False, []],
		"Four of a kind": [False, []],
		"Full house": [False, []],
		"Flush": [False, []],
		"Straight": [False, []],
		"Three of a kind": [False, []],
		"Two pair": [False, []],
		"Pair": [False, []],
		"High card": [False, []]
	}

def check_straight(all_cards):
	#print("running straight function")
	straight = False
	straight_hand = []
	for x in range(len(all_cards)-4):
		count = 0
		temp_hand = all_cards[x:x+5]

		for index in range(len(temp_hand)-1):
			if temp_hand[index+1][0] == temp_hand[index][0]-1:
				count += 1

		if count == 4:
			straight = True
			straight_hand = temp_hand
			break

	#Check case where Ace is the low card
	if not straight:
		#14 (which represents ace) now replaced with 1
		a_cards_m = [(1, x[1]) if x[0]==14 else x for x in all_cards]
		a_cards_m.sort(reverse = True)

		for x in range(len(a_cards_m)-4):
			temp_hand = a_cards_m[x:x+5]
			if temp_hand[0][0] == 5 and temp_hand[1][0] == 4 \
			and temp_hand[2][0] == 3 and temp_hand[3][0] == 2 \
			and temp_hand[4][0] == 1:
				straight = True
				straight_hand = temp_hand
				break

	return straight, conv_to_rank_suit(straight_hand)


def check_flush(all_cards):
	flush = False
	flush_hand = []
	unique = Counter([x[1] for x in all_cards])
	common_cards = unique.most_common(1)
	com_suit = common_cards[0][0]

	if common_cards[0][1] >= 5:
		flush = True
		flush_hand = [x for x in all_cards if x[1] == com_suit]

	return flush, conv_to_rank_suit(flush_hand[:5])


def check_straight_flush(all_cards):
	#print("running straight flush function")

	straight_flush = False
	straight_flush_hand = []

	unique = Counter([x[1] for x in all_cards])

	#From counter obj, take the most common occuring suit
	common_cards = unique.most_common(1)
	com_suit = common_cards[0][0]

	if common_cards[0][1] < 5:
		#you don't even have a flush
		return False, []

	all_cards = [x for x in all_cards if x[1] == com_suit]


	#Shortcut to evaluate when aces are low as well as high:
	#create new array where aces are value 1 and append to
	#all_cards, so low and high both evaulated.
	aces_one = [(1, x[1]) for x in all_cards if x[0] == 14]
	all_cards = all_cards + aces_one

	for x in range(len(all_cards)-4):
		temp_hand = all_cards[x:x+5]
		#print("temp hand ", temp_hand)
		flush, flush_hand = check_flush(temp_hand)
		straight, straight_hand = check_straight(temp_hand)
		if not (flush and straight):
			continue
		#print(straight_hand, " and ", flush_hand)
		assert set(straight_hand) == set(flush_hand), "Different hands being evaluated"
		if straight and flush:
			straight_flush = True
			straight_flush_hand = straight_hand
			break

	return straight_flush, conv_to_rank_suit(straight_flush_hand)



def check_four_kind(all_cards):
	#print("running four of a kind function")
	four_kind = False
	four_kind_hand = []
	unique = Counter([x[0] for x in all_cards])
	#creates a counter object of format var, count ({10: 4, 14: 1, })
	common_card = unique.most_common(1)[0]
	if common_card[1] == 4:
		four_kind = True
		four_kind_hand = [x for x in all_cards if x[0] == common_card[0]]


	for card in all_cards:
		if card[0] != common_card[0]:
			four_kind_hand.append(card)
			break

	return four_kind, conv_to_rank_suit(four_kind_hand)




def check_full_house(all_cards):
	#print("running full house function")
	full_house = False
	full_house_hand = []
	unique = Counter([x[0] for x in all_cards])
	common_cards = unique.most_common(2)

	assert common_cards[0][1] <= 3, "Most common occurence exceeded 3"

	if common_cards[0][1] == 3 and common_cards[1][1] >= 2:
		full_house = True
		largest = common_cards[0][0]
		smallest = common_cards[1][0]


		if common_cards[0][1] == common_cards[1][1]:
			largest = max(common_cards[0][0], common_cards[1][0])
			smallest = min(common_cards[0][0], common_cards[1][0])


		three_kind = [x for x in all_cards if x[0] == largest]
		assert len(three_kind) == 3, "Your three kind len is wrong"

		pair = [x for x in all_cards if x[0] == smallest]

		full_house_hand = three_kind + pair[:2]

	return full_house, conv_to_rank_suit(full_house_hand)



def check_three_kind(all_cards):
	#print("running three of a kind function")
	three_kind = False
	three_kind_hand = []
	unique = Counter([x[0] for x in all_cards])
	common_card = unique.most_common(1)[0]

	if common_card[1] == 3:
		three_kind = True
		three_kind_hand = [x for x in all_cards if x[0] == common_card[0]]

		remainder = [x for x in all_cards if x[0] != common_card[0]]

		three_kind_hand += remainder[:2]

	return three_kind, conv_to_rank_suit(three_kind_hand)



def check_two_pair(all_cards):
	#print("running two pair function")
	two_pair = False
	two_pair_hand = []
	unique = Counter([x[0] for x in all_cards])
	common_cards = unique.most_common(2)

	if common_cards[0][1] == 2 and common_cards[1][1] == 2:
		two_pair = True
		two_pair_hand += [x for x in all_cards if x[0] == common_cards[0][0]]
		two_pair_hand += [x for x in all_cards if x[0] == common_cards[1][0]]

		for card in all_cards:
			if card[0] != common_cards[0][0] and card[0] != common_cards[1][0]:
				two_pair_hand.append(card)
				break

	return two_pair, conv_to_rank_suit(two_pair_hand)



def check_pair(all_cards):
	#print("running pair function")
	pair = False
	pair_hand = []
	unique = Counter([x[0] for x in all_cards])
	common_card = unique.most_common(1)[0]

	if common_card[1] == 2:
		pair = True
		pair_hand = [x for x in all_cards if x[0] == common_card[0]]

		assert len(pair_hand) == 2, "Something not right with your pair"

		for card in all_cards:
			if card[0] != common_card[0]:
				pair_hand.append(card)
				if len(pair_hand) == 5:
					break

	return pair, conv_to_rank_suit(pair_hand)



def hand_value_check(hole_cards, *board):

	if len(hole_cards[0]) != 2:
		raise_value_error("You need to include hole cards as a \
tuple.")

	board_list = hole_cards + board

	#Exception handling to catch repeats.
	#set removes all duplicates, list length then compared.
	if len(board_list) != len(set(board_list)):
		raise_value_error("You have repeated cards")
	if len(board_list) < 5 or len(board_list) > 7:
		raise_value_error("Too many/few cards, make sure \
you have between 5 and 7 cards, including hole cards in brackets.")
	for card in board_list:
		if len(card) != 2:
			raise_value_error("Card format is two \
characters per card eg for six of hearts\
use 6h (from ten onwards use letters: Th, Kd")
		elif not card[1:].isalpha():
			raise_value_error("incorrect format: one charcter\
				for rand and one letter for suit, eg 8s")
		elif not (card[1:].upper() == 'S' or card[1:].upper() == 'H'\
			or card[1:].upper() == 'C' or card[1:].upper() == 'D'):
			raise_value_error("cannot identify suit")



	#board_list.sort(reverse = True)

	# if len(board_list) == 5: print("You are on the flop")
	# elif len(board_list) == 6: print("You are on the turn")
	# elif len(board_list) == 7: print("You are on the river")
	# else: print("Incorrect number of cards specified.")
	#print("your hole cards are ", hole_cards[0], " and ", hole_cards[1])

	#Dictionary storing whether hand type is true/fase, and
	#storing the strongest 5 card hand in a list.

	c_board_list = convert_card(board_list)
	c_board_list.sort(reverse = True)


	hand_values["Straight flush"] = check_straight_flush(c_board_list)

	if not hand_values["Straight flush"][0]:
		hand_values["Four of a kind"] = check_four_kind(c_board_list)

	if not hand_values["Four of a kind"][0]:
		hand_values["Full house"] = check_full_house(c_board_list)

	if not hand_values["Full house"][0]:
		hand_values["Flush"] = check_flush(c_board_list)

	if not hand_values["Flush"][0]:
		hand_values["Straight"] = check_straight(c_board_list)

	if not hand_values["Straight"][0]:
		hand_values["Three of a kind"] = check_three_kind(c_board_list)

	if not hand_values["Three of a kind"][0]:
		hand_values["Two pair"] = check_two_pair(c_board_list)

	if not hand_values["Two pair"][0]:
		hand_values["Pair"] = check_pair(c_board_list)

	if not hand_values["Pair"][0]:
		hand_values["High card"] = True, c_board_list[:5]


	for key, x in hand_values.items():
		print(key, x[0])
		if x[0]:
			print("You have a ", key, " ", conv_to_rank_suit(x[1]))
			return key
			assert False, "This ran after return key"
			break


def hole_cards_to_board(best_hand, board):
	hole_cards = board[:2]
	print("you hole cards: ", hole_cards)
	hole_cards_used = False

	#Check if the best hand is using either of your hole cards

	for h_card in hole_cards:
		for card in best_hand:
			if h_card == card:
				hole_cards_used = True

	if not hole_cards_used:
		print("You have nothing: you're playing the board")




# Converts cards to a standard 3 char format:
# Eg 6H = 06,H   KC = 13,C
def convert_card(card_list):

	result = []

	#print("your card list: ", card_list)

	for card_value in card_list:

		card_value = card_value.upper()

		if card_value[:1] == 'T':
			card_value = '10' + card_value[1:]
		if card_value[:1] == 'J':
			card_value = '11' + card_value[1:]
		if card_value[:1] == 'Q':
			card_value = '12' + card_value[1:]
		if card_value[:1] == 'K':
			card_value = '13' + card_value[1:]
		if card_value[:1] == 'A':
			card_value = '14' + card_value[1:]

		if len(card_value) > 2:
			result.append((int(card_value[:2]), card_value[-1:]))
		else:
			result.append((int(card_value[:1]), card_value[-1:]))

	return result

def conv_to_rank_suit(card_list):
	result = []

	for card in card_list:

		if card[0] == 14:
			result.append('A' + card[1].lower())
		elif card[0] == 1:
			result.append('A' + card[1].lower())
		elif card[0] == 13:
			result.append('K' + card[1].lower())
		elif card[0] == 12:
			result.append('Q' + card[1].lower())
		elif card[0] == 11:
			result.append('J' + card[1].lower())
		elif card[0] == 10:
			result.append('T' + card[1].lower())
		else:
			result.append(str(card[0]) + card[1].lower())

	return result

def raise_value_error(message):
	try:
		raise ValueError(message)
	except Exception as error:
		print(repr(error))
	sys.exit()


#hand_value_check(('5s'), '5h', '5d', '3d')
#hand_value_check(('bc', '6c'), '3c', '4c', '2c')
#hand_value_check(('Ac', 'Jc'), '6d', 'As', '8s', '4s', 'Ad')




