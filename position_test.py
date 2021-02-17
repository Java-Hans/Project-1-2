import cv2
import numpy as np
import pyautogui
from cardrecog2 import CardRecog2
from Player import Player
from hand_strength import hand_value_check
import time

# from hand_strength import HandStrength

img_gray = pyautogui.screenshot()
img_gray = cv2.cvtColor(np.array(img_gray), cv2.COLOR_RGB2GRAY)
x1, x2 = 0, 800
y1, y2 = 0, 580
cropped_img = img_gray[y1:y2, x1:x2]
bx1, bx2 = int(0.25 * x2), int(0.75 * x2)  # crop x coordinates for board (flop - river)
by1, by2 = int(0.3 * y2), int(0.5 * y2)  # crop y coordinates for board (flop - river)
cards_back_template = cv2.imread('images2/base_img/cards.png', 0)
board_path = 'images2/board_cards.png'

position_names = ['Dealer', 'SB', 'BB', 'UTG',
                  'UTGp1', 'Mid Pos 1', 'Mid Pos 2', 'Lojack', 'Hijack', 'Cutoff']
table_size = 10

# board_cards = cropped_img[by1:by2, bx1:bx2]
# cv2.imwrite(board_path, board_cards)

# cv2.imshow('board cards',board_cards)
# cv2.waitKey(0)
##board_path = 'images2/board_cards.png'
board_obj = CardRecog2(board_path)
board_list = board_obj.read_board_cards()

myself = Player('P Seat')
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

# hole_cards = cropped_img[int(y2 * cy1):int(y2 * cy2),
#              int(x2 * cx1):int(x2 * cx2)]
# cv2.imwrite('my_hole_cards.png', hole_cards)
# card_recog_obj = CardRecog2('my_hole_cards.png')

# def show_position(cx1, cx2, cy1, cy2):
#     i_height, i_width = cropped_img.shape[:2]
#     cropped_window = cropped_img[int(cy1 * i_height):int(cy2 * i_height), int(cx1 * i_width):int(cx2 * i_width)]
#     cv2.imshow('small window', cropped_window)
#     cv2.waitKey(0)


# show_position(0.04, 0.22, 0.12, 0.32)




# cv2.imshow('my hole cards', hole_cards)
# cv2.waitKey(0)

def show_window(an_image):
    cv2.imshow('the window', an_image)
    cv2.waitKey(0)


def find_button6(the_image):
    template = cv2.imread('images2/base_img/button.png', 0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(the_image, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.85
    loc = np.where(res >= threshold)
    match_list = list(zip(*loc[::-1]))

    for pt in zip(*loc[::-1]):
        cv2.circle(the_image, (pt[0], pt[1]), radius=5, color=(255, 255, 255), thickness=5)
        # print('location: ' + str(pt[0]) + " " + str(pt[1]))

        if pt[0] > int(0.67 * x2) and pt[1] < int(0.41 * y2):
            print('button at NE')
        elif pt[0] > int(0.67 * x2) and pt[1] >= int(0.41 * y2):
            print('button at SE')
        elif int(0.31 * x2) < pt[0] <= int(0.67 * x2) and pt[1] > int(0.42 * y2):
            print('button at S')
        elif int(0.31 * x2) < pt[0] <= int(0.67 * x2) and pt[1] < int(0.42 * y2):
            print('button at N')
        elif pt[0] < int(0.31 * x2) and pt[1] < int(0.41 * y2):
            print('button at NW')
        elif pt[0] < int(0.31 * x2) and pt[1] >= int(0.41 * y2):
            print('button at SW')
        else:
            print('something wrong with button areas')


def find_button10(the_image):
    template = cv2.imread('images2/base_img/button.png', 0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(the_image, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.85
    loc = np.where(res >= threshold)
    match_list = list(zip(*loc[::-1]))

    for pt in zip(*loc[::-1]):
        # marks location of button on image (for reference purposes)
        # cv2.circle(cropped_img, (pt[0], pt[1]), radius=5, color=(255, 255, 255), thickness=5)
        # print('location: ' + str(pt[0]) + " " + str(pt[1]))

        if int(0.49 * x2) >= pt[0] > int(0.36 * x2) and pt[1] > int(0.4 * y2):
            myself.set_position(position_names[0])
            # print('You are the button')
            return 0
        elif pt[0] < int(0.36 * x2) and pt[1] > int(0.48 * y2):
            seat_one.set_position(position_names[0])
            return 1
            # print('button at position 1')
        elif pt[0] < int(0.25 * x2) and int(0.36 * y2) < pt[1] < int(0.48 * y2):
            seat_two.set_position(position_names[0])
            return 2
            # print('button at position 2')
        elif pt[0] < int(0.25 * x2) and pt[1] < int(0.36 * y2):
            seat_three.set_position(position_names[0])
            return 3
            # print('button at position 3')
        elif int(0.28 * x2) < pt[0] < int(0.49 * x2) and pt[1] < int(0.33 * y2):
            seat_four.set_position(position_names[0])
            return 4
            # print('button at position 4')
        elif int(0.49 * x2) < pt[0] < int(0.7 * x2) and pt[1] < int(0.33 * y2):
            seat_five.set_position(position_names[0])
            return 5
            # print('button at position at 5')
        elif pt[0] > int(0.7 * x2) and pt[1] < int(0.36 * y2):
            seat_six.set_position(position_names[0])
            return 6
            # print('button at position 6')
        elif pt[0] > int(0.7 * x2) and int(0.36 * y2) < pt[1] < int(0.48 * y2):
            seat_seven.set_position(position_names[0])
            return 7
            # print('button at position 7')
        elif pt[0] > int(0.62 * x2) and pt[1] > int(0.48 * y2):
            seat_eight.set_position(position_names[0])
            return 8
            # print('button at position 8')
        elif int(0.49 * x2) < pt[0] < int(0.62 * x2) and pt[1] > int(0.57 * y2):
            seat_nine.set_position(position_names[0])
            return 9
            # print('button at positon 9')
        else:
            print('something wrong, cant find button')
            return -1


# find_button10()


def crop_and_match2(description, the_image, the_threshold, the_template, crop_coord):
    any_match = False
    i_height, i_width = the_image.shape[:2]
    cx1, cx2, cy1, cy2 = crop_coord[0], crop_coord[1], crop_coord[2], crop_coord[3]
    cropped_window = the_image[int(cy1 * i_height):int(cy2 * i_height), int(cx1 * i_width):int(cx2 * i_width)]
    match_result = cv2.matchTemplate(cropped_window, the_template, cv2.TM_CCOEFF_NORMED)
    match_location = np.where(match_result >= the_threshold)
    list_of_match = list(zip(*match_location[::-1]))
    if not list_of_match:
        # print('no one at ' + description)
        any_match = False
    else:
        # print('player at ' + description)
        any_match = True
    # cv2.imshow(description, cropped_window)
    # cv2.waitKey(0)

    return any_match


def count_active_players2(the_image, hole_card_obj):
    active_players = 0
    myself_active, my_hole_cards = hole_card_obj.match_hole_cards()
    for player in seat_list:

        if crop_and_match2(player.get_seat_number(), the_image, 0.85, cards_back_template,
                           player.get_hole_card_crop()):
            active_players += 1
            player.set_active(True)
        else:
            player.set_active(False)
    if myself_active:
        myself.set_active(True)
        active_players += 1
        myself.set_hole_cards(my_hole_cards)
        # print(f'yolo hole cards {myself.get_hole_cards()}')
    else:
        myself.set_active(False)

    return active_players


# def find_button_seat(list_seats):
#     for a_seat in list_seats:
#         if a_seat.get_position() == position_names[0]:
#             return list_seats.index(a_seat)

def test_assign_positions(btn_index):
    pos_index = 1
    for p in range(1, table_size):
        if seat_list[(btn_index + p) % table_size].get_active():
            seat_list[(btn_index + p) % table_size].set_position(position_names[pos_index])
            pos_index += 1


old_button = None
new_button = None

for x in range(12):
    the_time = str(round(time.time()))
    img_gray2 = pyautogui.screenshot()
    img_gray2 = cv2.cvtColor(np.array(img_gray2), cv2.COLOR_RGB2GRAY)
    cropped_img2 = img_gray2[y1:y2, x1:x2]
    cv2.imwrite('images2/' + the_time + '.png', cropped_img2)

    board_cards2 = cropped_img2[by1:by2, bx1:bx2]
    cv2.imwrite(board_path, board_cards2)
    # cv2.imshow('board cards',board_cards)
    # cv2.waitKey(0)
    ##board_path = 'images2/board_cards.png'
    board_obj = CardRecog2(board_path)
    board_list = board_obj.read_board_cards()

    hole_cards2 = cropped_img2[int(y2 * cy1):int(y2 * cy2),
                 int(x2 * cx1):int(x2 * cx2)]
    cv2.imwrite('my_hole_cards.png', hole_cards2)
    card_recog_obj2 = CardRecog2('my_hole_cards.png')

    print(f'board cards: {board_list}')
    num_active_players = count_active_players2(cropped_img2, card_recog_obj2)
    my_h_cards = myself.get_hole_cards() if myself.active else None

    print(f'Players active: {num_active_players}')
    # print(f'yo ho hole cards: {myself.get_hole_cards()}') if myself.active else print('player not active')
    print(my_h_cards)
    new_button = find_button10(cropped_img2)
    # h_strength_obj = HandStrength
    print(f'Button seat location: {new_button}')
    # checking we are on the same hand using the button. If same hand, don't reassign seats if players have folded.
    if new_button != old_button:
        test_assign_positions(new_button)
    old_button = new_button
    for seat in seat_list:
        print(str(seat.get_seat_number()) + ' ' + str(seat.get_position()) + ',\t\t Active: ' + str(seat.get_active()))

    # print(hole_cards)
    # print(*board_list)

    h_values, my_b_hand = None, None

    if len(board_list) >= 3 and myself.active:
        h_values, my_b_hand = hand_value_check(myself.get_hole_cards(), *board_list)

    with open("Output.txt", "a") as text_file:
        text_file.write(the_time + '\n')
        text_file.write(f'Board cards:\t\t {board_list}\n')
        text_file.write(f'Players active:\t\t {num_active_players}\n')
        text_file.write(f'My Hole cards:\t\t {my_h_cards}\n')
        text_file.write(f'Button index location\t {new_button}\n')
        for seat in seat_list:
            text_file.write(str(seat.get_seat_number()) + ' ' + str(seat.get_position()) + ',\t\t Active: ' + str(
                seat.get_active()) + '\n')
        if len(board_list) >= 3 and myself.active:
            for key, x in h_values.items():
                text_file.write(f'{key}, {x[0]}\n')
                if x[0]:
                    break
            text_file.write(str(my_b_hand) + '\n')
        text_file.write(f'---------------------------------\n\n')
    time.sleep(6)

        # for i in range(2):
        #     text_file.write(f"a number: {i}\n")
