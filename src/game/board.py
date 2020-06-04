import json

import cv2 as cv
import numpy as np
import pyautogui
from pytesseract import pytesseract
import requests

from game.Line import Line
from game.cvutil import CvUtil

POSITION_TUPLE_X_Y = (0,68)
POSITION_TUPLE_W_H = (200,200)

LINE_TUPLE_X_Y=(26,108)
LINE_TUPLE_W_H=(321,25)
class Board:
    def __init__(self,board_sprites,arrow_sprites,display):
        self.board_sprites_matching = board_sprites
        self.size="Unknown"
        self.hint_number=0
        self.arrow_sprites = arrow_sprites
        self.board = self.init(self.take_screen())
        print("BOARD WITH : "+str(self.hint_number)+"hints")
        self.pos = self.find_pos()
        self.splited_lines = self.split_board()
        self.hint_list= self.find_lines()
        self.pos_list=[self.pos]
        self.display = display
        self.refresh_display()
        with open('../indice.json') as json_file:
            self.json_hint= json.load(json_file)


    def init(self,dofus_screen):
            sixhint = cv.matchTemplate(dofus_screen, self.board_sprites_matching[0], cv.TM_CCOEFF_NORMED)
            fourhint = cv.matchTemplate(dofus_screen, self.board_sprites_matching[1], cv.TM_CCOEFF_NORMED)
            one_hint = cv.matchTemplate(dofus_screen, self.board_sprites_matching[2], cv.TM_CCOEFF_NORMED)
            fivehint = cv.matchTemplate(dofus_screen, self.board_sprites_matching[3], cv.TM_CCOEFF_NORMED)
            twohint = cv.matchTemplate(dofus_screen, self.board_sprites_matching[4], cv.TM_CCOEFF_NORMED)

            Sixmin_val, Sixmax_val, Sixmin_loc, Sixmax_loc = cv.minMaxLoc(sixhint)
            fourmin_val, fourmax_val, fourmin_loc, fourmax_loc = cv.minMaxLoc(fourhint)
            onemin_val, onemax_val, onemin_loc, onemax_loc = cv.minMaxLoc(one_hint)
            fivemin_val, fivemax_val, fivemin_loc, fivemax_loc = cv.minMaxLoc(fivehint)
            twomin_val, twomax_val, twomin_loc, twomax_loc = cv.minMaxLoc(twohint)
            ##print('Best match top left position: %s' % str(max_loc))
            ##print('Best match confidence: %s' % max_val)
            threshold = 0.9
            if Sixmax_val > fourmax_val and Sixmax_val > fivemax_val and Sixmax_val > onemax_val and Sixmax_val > twomax_val:
                self.size = "normal"
                self.hint_number = 6
                return self.extract_board(dofus_screen, Sixmax_val, Sixmax_loc, self.board_sprites_matching[0])

            if onemax_val > fourmax_val and onemax_val > fivemax_val and onemax_val > Sixmax_val and onemax_val > twomax_val:
                self.size = "1small"
                self.hint_number = 1
                return self.extract_board(dofus_screen, onemax_val, onemax_loc, self.board_sprites_matching[2])
            if fivemax_val > fourmax_val and fivemax_val > onemax_val and fivemax_val > Sixmax_val and fivemax_val > twomax_val:
                self.size = "5small"
                self.hint_number = 5
                return self.extract_board(dofus_screen,fivemax_val,fivemax_loc,self.board_sprites_matching[3])

            if fourmax_val > fivemax_val and fourmax_val > onemax_val and fourmax_val > Sixmax_val and fourmax_val > twomax_val:
                self.size = "small"
                self.hint_number = 4
                return self.extract_board(dofus_screen, fourmax_val, fourmax_loc, self.board_sprites_matching[1])

            if twomax_val > fivemax_val and twomax_val > onemax_val and twomax_val > Sixmax_val and twomax_val > fourmax_val:
                self.size = "2small"
                self.hint_number = 2
                return self.extract_board(dofus_screen, twomax_val, twomax_loc, self.board_sprites_matching[4])

    def take_screen(self):
        dofus = pyautogui.screenshot()
        dofus = cv.cvtColor(np.array(dofus), cv.COLOR_RGB2BGR)
        return dofus
    ##not used
    def old_find_pos(self, image):
        res = CvUtil.extract_rectangle_from_image(image, POSITION_TUPLE_X_Y[0], POSITION_TUPLE_X_Y[1],
                                                POSITION_TUPLE_W_H[0],
                                                POSITION_TUPLE_W_H[1])
        print(pytesseract.image_to_string(res))
        return res

    def find_pos(self):
        pos_text = pytesseract.image_to_string(self.board)
        locate = pos_text[pos_text.index('Départ') + 1:-1]
        posstr = locate[locate.index('[')+1:locate.index(']')]
        pos = posstr.split(",")
        res = (pos[0],pos[1])
        print(res)
        return res

    def find_arrow(self,image):
        height, width = image.shape[:2]
        resultUp = cv.matchTemplate(image, self.arrow_sprites[0], cv.TM_CCOEFF_NORMED)
        resultRight = cv.matchTemplate(image, self.arrow_sprites[1], cv.TM_CCOEFF_NORMED)
        resultDown = cv.matchTemplate(image, self.arrow_sprites[2], cv.TM_CCOEFF_NORMED)
        resultLeft = cv.matchTemplate(image, self.arrow_sprites[3], cv.TM_CCOEFF_NORMED)
        resultUNKNOWN = cv.matchTemplate(image, self.arrow_sprites[4], cv.TM_CCOEFF_NORMED)


        min_valUp, max_valUp, min_locUp, max_locUp= cv.minMaxLoc(resultUp)
        min_valRight, max_valRight, min_locRight, max_locRight = cv.minMaxLoc(resultRight)
        min_valDown, max_valDown, min_locDown, max_locDown = cv.minMaxLoc(resultDown)
        min_valLeft, max_valLeft, min_locLeft, max_locLeft = cv.minMaxLoc(resultLeft)
        min_valUNKNOWN, max_valUNKNOWN, min_locUNKNOWN, max_locUNKNOWN = cv.minMaxLoc(resultUNKNOWN)

        ##print("UP" +str(max_valUp))
        ##print("Down" + str(max_valDown))
        ##print("Right" + str(max_valRight))
        ##print("Left" + str(max_valLeft))
        ##print("Unkown" + str(max_valUNKNOWN))

        if max_valUp>max_valRight and max_valUp>max_valDown and max_valUp>max_valLeft and max_valUp>max_valUNKNOWN:
            return "top"

        if max_valLeft>max_valRight and max_valLeft>max_valDown and max_valLeft>max_valUp and max_valLeft>max_valUNKNOWN :
            return "left"

        if max_valDown > max_valRight and max_valDown > max_valLeft  and max_valDown > max_valUp and  max_valDown>max_valUNKNOWN :
            return "bottom"

        if max_valRight > max_valDown and max_valRight > max_valLeft  and max_valRight > max_valUp and max_valRight>max_valUNKNOWN :
            return "right"

        if max_valUNKNOWN > max_valDown and max_valUNKNOWN > max_valLeft  and max_valUNKNOWN > max_valUp and max_valUNKNOWN > max_valRight:
            return "UNKNOWN"

    def find_lines(self):
        line_list = []
        for i in range(len(self.splited_lines)):
            direction = self.find_arrow(self.splited_lines[i])
            if direction == "UNKNOWN":
                line_list.append(Line("UNKNOWN", "?"))
            else:
                text = pytesseract.image_to_string(self.splited_lines[i])
                start = text.index(' ')
                if text[0].isalpha():
                    start = -1
                line = text.partition('\n')[0]
                hint = self.word_checker(line[start + 1:])
                line_list.append(Line(direction, hint))
        return line_list

    def split_board(self):
        offsetw=0
        offsety=0
        if self.size =="1small":
            offsety=+5
        elif self.hint_number ==2:
            offsetw=25
        list = []
        z = 1
        height, width = self.board.shape[:2]
        i = LINE_TUPLE_X_Y[1]-offsety
        while i < height - (LINE_TUPLE_W_H[1] * 2):
            line = CvUtil.extract_rectangle_from_image(self.board, LINE_TUPLE_X_Y[0], i, LINE_TUPLE_W_H[1],
                                                       LINE_TUPLE_W_H[0]-offsetw)
            CvUtil.save_image("line" + str(z) + ".jpg", line)
            z += 1
            i += LINE_TUPLE_W_H[1] + z
            list.append(line)
        return list

    def printMyState(self):
        print("There is "+str(self.hint_number)+" hints")
        for line in self.hint_list:
            print(line)

    def lastHintKnownIndex(self):
        if len(self.hint_list)==1:
            return 0
        i=0
        for line in self.hint_list:
            if line.indice== '?':
                return i-1
            i+=1
        return len(self.hint_list)-1
    
    def lastHintKnown(self):
        return self.hint_list[self.lastHintKnownIndex()]

    def next_step(self,posx=999,posy=999):
        self.refresh()
        if self.lastHintKnownIndex()+1!= len(self.pos_list):
            print("PLEASE GO TO THE NEXT HINT")
            return
        last_hint = self.lastHintKnown()
        if 'Phorreur' in last_hint.indice:
            print("phoreurrrrrr")
            if posx!=999 and posy!=999:
                self.pos_list.append((posx,posy))
                self.refresh_display()
            return
        uri_request = 'https://dofus-map.com/huntTool/getData.php?x=' + str(self.pos_list[-1][0]) + '&y=' + str(self.pos_list[-1][1]) + '&direction='+last_hint.direction+'&world=0&language=fr'
        print(uri_request)
        r = requests.get(uri_request)
        print(r.text)
        res = r.json()
        print(last_hint)
        print(res["hints"])
        for indince in res["hints"]:
            if last_hint.indice == self.json_hint[str(indince["n"])]:
                print(self.json_hint[str(indince["n"])]+'  X :'+str(indince['x'])+'   Y :'+ str(indince['y']))
                self.pos_list.append((str(indince['x']),str(indince['y'])))
        self.refresh_display()

    def refresh(self):
        self.board = self.init(self.take_screen())
        ##self.pos = self.find_pos()
        self.splited_lines = self.split_board()
        self.hint_list = self.find_lines()
    def refresh_display(self):
        for i in self.display.get_children():
            self.display.delete(i)
        self.display.insert('', 'end', iid=0, values=('Départ', self.pos_list[0],'.'))
        i = 1
        for hint in self.hint_list:
            if i>=len(self.pos_list):
                self.display.insert('', 'end', iid=i, values=(hint.indice, '?',hint.direction))
            else:
                self.display.insert('', 'end', iid=i, values=(hint.indice, self.pos_list[i],hint.direction))
            i+=1

    def word_checker(self,word):
        bugged_word = {"quinerepoussepas": "Souche qui ne repousse pas", "Stéle en pierre": "Stèle en pierre"}
        for key in bugged_word:
            if key in word:
                return bugged_word[key]
        return word


    def extract_board(self,dofus_screen,max_val,max_loc,board_sprite):
        threshold = 0.9
        ##print('Best match top left position: %s' % str(max_loc))
        ##print('Best match confidence: %s' % max_val)

        if max_val >= threshold:
            ##print('Found needle.')

            # Get the size of the needle image. With OpenCV images, you can get the dimensions
            # via the shape property. It returns a tuple of the number of rows, columns, and
            # channels (if the image is color):
            needle_w = board_sprite.shape[1]
            needle_h = board_sprite.shape[0]

            # Calculate the bottom right corner of the rectangle to draw
            top_left = max_loc
            bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)

            # Draw a rectangle on our screenshot to highlight where we found the needle.
            # The line color can be set as an RGB tuple
            cv.imwrite('board.jpg',
                       dofus_screen[top_left[1]:top_left[1] + needle_h, top_left[0]:top_left[0] + needle_w])

            # self.print_result_matching(image,top_left,bottom_right)
            return dofus_screen[top_left[1]:top_left[1] + needle_h, top_left[0]:top_left[0] + needle_w]