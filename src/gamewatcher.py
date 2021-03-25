import win32gui

import cv2 as cv
import numpy as np
from PIL import ImageGrab

from cvutil import CvUtil

POSITION_TUPLE_X_Y = (0,68)
POSITION_TUPLE_W_H = (200,200)

LINE_TUPLE_X_Y=(16,108)
LINE_TUPLE_W_H=(321,25)
class GameWatcher:

    def __init__(self,board):
        self.board=board


    def take_dofus_screenshot(self):


        toplist, winlist = [], []

        def enum_cb(hwnd, results):
            winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

        win32gui.EnumWindows(enum_cb, toplist)

        dofus = [(hwnd, title) for hwnd, title in winlist if 'Kalfa - Dofus 2.55.8.11'.lower() in title.lower()]
        # just grab the hwnd for first window matching firefox
        dofus = dofus[0]
        hwnd = dofus[0]

        win32gui.SetForegroundWindow(hwnd)
        bbox = win32gui.GetWindowRect(hwnd)
        img = ImageGrab.grab(bbox).convert('RGB')
        pic = np.array(img.getdata()).reshape(img.size[0], img.size[1], 3)
        pic = pic[:, :, ::-1].copy()
        return pic



    def find_board_pos(self,boardimg):
        pos  = CvUtil.extract_rectangle_from_image(boardimg,LINE_TUPLE_X_Y[0],76,LINE_TUPLE_W_H[1],LINE_TUPLE_W_H[0])
        cv.imwrite("poz.png",pos)
        return pos