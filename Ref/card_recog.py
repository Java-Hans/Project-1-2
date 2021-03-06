import cv2
import numpy as np

class card_recog:

	def __init__(self, img_path):
		self.img_path = img_path

	suits = ["Spades.png", "Hearts.png", "Diamonds.png", "Clubs.png"]
	card_numbers = ["A.png", "2.png", "3.png", "4.png", "5.png", "6.png",\
			"7.png", "8.png", "9.png", "10.png", "J.png", "Q.png", "K.png"]

	def t_matching(self, t_list,threshold):
		#img_rgb = cv2.imread('images/0_PP_shot_full_9d4h.png')
		#img_rgb = cv2.imread('/Users/Hans/Documents/Coding/Python_workspace/Poker_bot2/my_pyton_screenshot9jpg')
		img_rgb = cv2.imread(self.img_path)
		img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

		result = []

		for t_file in t_list:
			template = cv2.imread('images/base_img/' + t_file,0)
			w, h = template.shape[::-1]

			res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
			loc = np.where( res >= threshold) #0.9 for numbers, 0.97 for suits

			match_list = list(zip(*loc[::-1]))

			# Only execute the rest of the loop if there is a match
			if len(match_list) == 0:
				continue

			# Now to filter the duplicate matches that are a few pixels apart.	
			new_match_list = []

			for sloc in match_list:
				repeat = False

				if not new_match_list:
					new_match_list.append(sloc)

				for sloc2 in new_match_list:
					if abs(sloc2[0] - sloc[0])/sloc[0] < 0.01:
						repeat = True

				if not repeat:
					new_match_list.append(sloc)

			#print("length of new match list", len(new_match_list))
				

			print("{} card(s) matched: {}".format(len(new_match_list),t_file[:-4]))

			min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

			#for pt in zip(*loc[::-1]):
			for pt in new_match_list:
			    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)
			    print("position using pt is: {} and value is {},\
	match percentage is {}".format(pt, t_file[:-4], max_val))
			    result.append((pt,t_file[:-4]))

			print("{}\n".format(cv2.minMaxLoc(res)))

		print("and the final list is {}".format(result))
		return result

		cv2.imshow('Detected',img_rgb)
		cv2.waitKey(0)

	def match_hole_cards(self):
		print("Running suit match")
		suit_result = self.t_matching(self.suits, 0.9)
		print("Running value match")
		card_number_result = self.t_matching(self.card_numbers, 0.9)

		print("suit result ", suit_result)
		print("card number result ", card_number_result)

		left_suit = ""
		right_suit = ""
		left_number = ""
		right_number = ""

		if len(suit_result) == 0 or len(card_number_result) == 0:
			print("No cards recognised")
			return

		#Assume the first item in list is the left card
		left_suit = suit_result[0][1]
		right_suit = suit_result[1][1]

		if suit_result[1][0][0] < suit_result[0][0][0]:
			right_suit = suit_result[0][1]
			left_suit = suit_result[1][1]

		left_number = card_number_result[0][1]
		right_number = card_number_result[1][1]

		if card_number_result[1][0][0] < card_number_result[0][0][0]:
			right_number = card_number_result[0][1]
			left_number = card_number_result[1][1]

		print("You have", left_number, "of", left_suit)
		print("and", right_number, "of", right_suit)



test_ins1 = card_recog('images/5_PP_shot_full_4djd.png')
#test_ins1 = card_recog('images/scrn2_corrected.jpg')
test_ins1.match_hole_cards()





