import cv2
import numpy as np
import pyautogui
from card_recog2 import card_recog2

img_gray = pyautogui.screenshot()
img_gray = cv2.cvtColor(np.array(img_gray), cv2.COLOR_RGB2GRAY)
x1, x2 = 0, 800
y1, y2 = 0, 580
cropped_img = img_gray[y1:y2, x1:x2]
cards_back_template = cv2.imread('images2/base_img/cards.png', 0)
cv2.imwrite('images2/window.png', cropped_img)

# seats_list_6 = []
# seats_list_6.append(['south', 0.41, 0.6, 0.58, 0.8])
# seats_list_6.append(['south west', 0.02, 0.2, 0.43, 0.63])
# seats_list_6.append(['northwest', 0.02, 0.17, 0.17, 0.35])
# seats_list_6.append(['north', 0.39, 0.6, 0.02, 0.22])
# seats_list_6.append(['north east', 0.79, 0.99, 0.17, 0.34])
# seats_list_6.append(['south east', 0.82, 0.99, 0.43, 0.63])

# seats_window_10 = []
# seats_window_10.append(['Player seat', 0.27, 0.46, 0.57, 0.79])
# seats_window_10.append(['seat one', 0.04, 0.22, 0.49, 0.7])
# seats_window_10.append(['seat two', 0, 0.19, 0.3, 0.51])
# seats_window_10.append(['seat three', 0.04, 0.22, 0.12, 0.32])
# seats_window_10.append(['seat four', 0.23, 0.41, 0.04, 0.22])
# seats_window_10.append(['seat five', 0.6, 0.78, 0.04, 0.22])
# seats_window_10.append(['seat six', 0.8, 0.98, 0.13, 0.31])
# seats_window_10.append(['seat seven', 0.81, 0.99, 0.32, 0.5])
# seats_window_10.append(['seat eight', 0.77, 0.95, 0.51, 0.69])
# seats_window_10.append(['seat nine', 0.54, 0.74, 0.57, 0.79])

position_names = ['Dealer', 'Small Blind', 'Big Blind' 'UTG',
                  'UTGp1', 'Mid Pos 1', 'Mid Pos 2', 'Lojack', 'Hijack', 'Cutoff']
table_size = 10
players_active = 0

class Player:
    def __init__(self, seat_number):
        self.seat_number = seat_number
        self.active = False
        self.position = None

    def get_seat_number(self):
        return self.seat_number

    # takes a list in the form [x1, x2, y1, y2]
    def set_hole_card_crop(self, hold_card_crop):
        self.hole_card_crop = hold_card_crop

    def get_hole_card_crop(self):
        return self.hole_card_crop

    def set_active(self, active):
        self.active = active

    def get_active(self):
        return self.active

    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position

    def print_position(self):
        print(self.position)

    def print_active(self):
        print(self.active)

myself = Player('Player seat')
seat_one = Player('Seat 1')
seat_two = Player('Seat 2')
seat_three = Player('Seat 3')
seat_four = Player('Seat 4')
seat_five = Player('Seat 5')
seat_six = Player('Seat 6')
seat_seven = Player('Seat 7')
seat_eight = Player('Seat 8')
seat_nine = Player('Seat 9')
seat_list = [myself, seat_one, seat_two, seat_three, seat_four, seat_five, seat_six, seat_seven, seat_eight, seat_nine]

myself.set_hole_card_crop([0.27, 0.46, 0.57, 0.79])
seat_one.set_hole_card_crop([0.04, 0.22, 0.49, 0.7])
seat_two.set_hole_card_crop([0, 0.19, 0.3, 0.51])
seat_three.set_hole_card_crop([0.04, 0.22, 0.12, 0.32])
seat_four.set_hole_card_crop([0.23, 0.41, 0.04, 0.22])
seat_five.set_hole_card_crop([0.6, 0.78, 0.04, 0.22])
seat_six.set_hole_card_crop([0.8, 0.98, 0.13, 0.31])
seat_seven.set_hole_card_crop([0.81, 0.99, 0.32, 0.5])
seat_eight.set_hole_card_crop([0.77, 0.95, 0.51, 0.69])
seat_nine.set_hole_card_crop([0.54, 0.74, 0.57, 0.79])

hole_card_coord = myself.get_hole_card_crop()
cx1, cx2, cy1, cy2 = hole_card_coord[0], hole_card_coord[1], hole_card_coord[2], hole_card_coord[3]

hole_cards = cropped_img[int(y2 * cy1):int(y2 * cy2),
             int(x2 * cx1):int(x2 * cx2)]


# myself.set_active(True)
# if myself.active:
#     print('hello active')
# else:
#     print('not active')
# myself.print_active()





def show_position(cx1, cx2, cy1, cy2):
    i_height, i_width = cropped_img.shape[:2]
    cropped_window = cropped_img[int(cy1 * i_height):int(cy2 * i_height), int(cx1 * i_width):int(cx2 * i_width)]
    cv2.imshow('small window', cropped_window)
    cv2.waitKey(0)

#show_position(0.04, 0.22, 0.12, 0.32)

cv2.imwrite('my_hole_cards.png', hole_cards)
card_recog_obj = card_recog2('my_hole_cards.png')
# cv2.imshow('my hole cards', hole_cards)
# cv2.waitKey(0)

def show_window(an_image):
    cv2.imshow('the window', an_image)
    cv2.waitKey(0)

def find_button6():
    template = cv2.imread('images2/base_img/button.png',0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(cropped_img,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.85
    loc = np.where(res >= threshold)
    match_list = list(zip(*loc[::-1]))

    for pt in zip(*loc[::-1]):
        cv2.circle(cropped_img, (pt[0], pt[1]), radius=5, color=(255, 255, 255), thickness=5)
        #print('location: ' + str(pt[0]) + " " + str(pt[1]))

        if pt[0] > int(0.67*x2) and pt[1] < int(0.41*y2):
            print('button at NE')
        elif pt[0] > int(0.67*x2) and pt[1] >= int(0.41*y2):
            print('button at SE')
        elif int(0.31*x2) < pt[0] <= int(0.67*x2) and pt[1] > int(0.42*y2):
            print('button at S')
        elif int(0.31*x2) < pt[0] <= int(0.67*x2) and pt[1] < int(0.42*y2):
            print('button at N')
        elif pt[0] < int(0.31*x2) and pt[1] < int(0.41*y2):
            print('button at NW')
        elif pt[0] < int(0.31 * x2) and pt[1] >= int(0.41 * y2):
            print('button at SW')
        else:
            print('something wrong with button areas')

def find_button10():
    template = cv2.imread('images2/base_img/button.png',0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(cropped_img,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.85
    loc = np.where(res >= threshold)
    match_list = list(zip(*loc[::-1]))

    for pt in zip(*loc[::-1]):
        #marks location of button on image (for reference purposes)
        #cv2.circle(cropped_img, (pt[0], pt[1]), radius=5, color=(255, 255, 255), thickness=5)
        print('location: ' + str(pt[0]) + " " + str(pt[1]))

        if int(0.49*x2) >= pt[0] > int(0.36*x2) and pt[1] > int(0.4*y2):
            myself.set_position(position_names[0])
            #print('You are the button')
        elif pt[0] < int(0.36*x2) and pt[1] > int(0.48*y2):
            seat_one.set_position(position_names[0])
            #print('button at position 1')
        elif pt[0] < int(0.25*x2) and int(0.36*y2) < pt[1] < int(0.48*y2):
            seat_two.set_position(position_names[0])
            #print('button at position 2')
        elif pt[0] < int(0.25*x2) and pt[1] < int(0.36*y2):
            seat_three.set_position(position_names[0])
            #print('button at position 3')
        elif int(0.28*x2) < pt[0] < int(0.49*x2) and pt[1] < int(0.33*y2):
            seat_four.set_position(position_names[0])
            #print('button at position 4')
        elif int(0.49*x2) < pt[0] < int(0.7*x2) and pt[1] < int(0.33*y2):
            seat_five.set_position(position_names[0])
            #print('button at position at 5')
        elif pt[0] > int(0.7*x2) and pt[1] < int(0.36*y2):
            seat_six.set_position(position_names[0])
            #print('button at position 6')
        elif pt[0] > int(0.7*x2) and int(0.36*y2) < pt[1] < int(0.48*y2):
            seat_seven.set_position(position_names[0])
            #print('button at position 7')
        elif pt[0] > int(0.62*x2) and pt[1] > int(0.48*y2):
            seat_eight.set_position(position_names[0])
            #print('button at position 8')
        elif int(0.49*x2) < pt[0] < int(0.62*x2) and pt[1] > int(0.57*y2):
            seat_nine.set_position(position_names[0])
            #print('button at positon 9')
        else:
            print('something wrong, cant find button')
find_button10()

for seat in seat_list:
    if seat.get_position() == position_names[0]:
        print(seat.get_seat_number() + '  jaaaaaaaa' + seat.get_position())


# def crop_and_match(description, the_image, the_threshold, the_template, cx1, cx2, cy1, cy2):
#     any_match = False
#     i_height, i_width = the_image.shape[:2]
#     cropped_window = the_image[int(cy1 * i_height):int(cy2 * i_height), int(cx1 * i_width):int(cx2 * i_width)]
#     match_result = cv2.matchTemplate(cropped_window, the_template, cv2.TM_CCOEFF_NORMED)
#     match_location = np.where(match_result >= the_threshold)
#     list_of_match = list(zip(*match_location[::-1]))
#     if not list_of_match:
#         print('no one at ' + description)
#         any_match = False
#     else:
#         print('player at ' + description)
#         any_match = True
#     # cv2.imshow(description, cropped_window)
#     # cv2.waitKey(0)
#
#     return any_match



def crop_and_match2(description, the_image, the_threshold, the_template, crop_coord):
    any_match = False
    i_height, i_width = the_image.shape[:2]
    cx1, cx2, cy1, cy2 = crop_coord[0], crop_coord[1], crop_coord[2], crop_coord[3]
    cropped_window = the_image[int(cy1 * i_height):int(cy2 * i_height), int(cx1 * i_width):int(cx2 * i_width)]
    match_result = cv2.matchTemplate(cropped_window, the_template, cv2.TM_CCOEFF_NORMED)
    match_location = np.where(match_result >= the_threshold)
    list_of_match = list(zip(*match_location[::-1]))
    if not list_of_match:
        print('no one at ' + description)
        any_match = False
    else:
        print('player at ' + description)
        any_match = True
    # cv2.imshow(description, cropped_window)
    # cv2.waitKey(0)

    return any_match



# def count_active_players():
#     active_players = 0
#     for k in positions_list_10:
#
#         if crop_and_match(k[0], cropped_img, 0.85, cards_back_template, k[1], k[2], k[3], k[4]):
#             active_players += 1
#     if card_recog_obj.match_hole_cards():
#         active_players += 1
#
#     print('Players active: ' + str(active_players))

def count_active_players2():
    active_players = 0
    for player in seat_list:

        if crop_and_match2(player.get_seat_number(), cropped_img, 0.85, cards_back_template,
                          player.get_hole_card_crop()):
            active_players += 1
            player.set_active(True)
    if card_recog_obj.match_hole_cards():
        myself.set_active(True)
        active_players += 1

    print('Players active: ' + str(active_players))
    return active_players
players_active = count_active_players2()

for the_player in seat_list:
    player_seat = the_player.get_seat_number()

    if the_player.get_active():
        print(the_player.get_seat_number() + ' is active')

button_index = -1
for player in seat_list:
    if player.get_position() == position_names[0]:
        button_index = seat_list.index(player)
        print('button indes: ' + str(button_index))

assigned_seats = 0
k = 1

# while assigned_seats < players_active:
#     if seat_list[(button_index+k)%table_size].get_active():
#         seat_list[(button_index+k)%table_size].set_position(position_names[1])
#         # print('index is ' + str((button_index+k)%table_size))
#         # print('is this even being run? ' + seat_list[(button_index+k)%table_size])
#         assigned_seats += 10
#
#     assigned_seats += 1

def find_small_blind():
    for k in range(1,table_size-1):
        if seat_list[(button_index + k) % table_size].get_active():
            seat_list[(button_index + k) % table_size].set_position(position_names[1])
            break
#find_small_blind()

def test_assign_positions():
    pos_index = 1
    for p in range(1,table_size):
        if seat_list[(button_index + p) % table_size].get_active():
            seat_list[(button_index + p) % table_size].set_position(position_names[pos_index])
            pos_index += 1
test_assign_positions()

for seat in seat_list:
    seat_pos = seat.get_position()
    if seat_pos == position_names[2]:
        print(seat.get_seat_number() + '  jaaaaaaaa' + seat_pos)

# for seat in seat_list:
#     print(str(seat.get_position()))