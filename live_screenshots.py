import numpy as np
import pyautogui
import imutils
import cv2
import time
from cardrecog2 import CardRecog2

while True:
    my_image = pyautogui.screenshot()
    my_image = cv2.cvtColor(np.array(my_image), cv2.COLOR_RGB2BGR)

    x1, x2 = 0, 550
    y1, y2 = 0, 800
    # image[y:y+h, x:x+w]
    cropped_img = my_image[x1:x2,y1:y2]
    hole_cards = my_image[round(0.5*x2):x2,round(0.4*y2):round(0.6*y2)]

    cv2.imwrite(("cropped_img.png"), cropped_img)
    cv2.imwrite(("hole_cards.png"), hole_cards)


    cv2.imshow("cropped", hole_cards)
    cv2.waitKey(1000)

    test_ins1 = CardRecog2('hole_cards.png')
    #test_ins1.match_hole_cards()
    if test_ins1.match_hole_cards():
        print('yes it is true')
    else:
        print('nooo false')
