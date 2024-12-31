import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from enum import Enum
import requests
from paddleocr import PaddleOCR, draw_ocr
from unidecode import unidecode
import pyautogui
from ppocr.utils.logging import get_logger
import  time
import logging
import re
from keyboard import press_and_release,press
import pyperclip as pc
import win32com.client as win
import win32gui
import win32process
from ahk import AHK
import gameWatcher as gw
import DofusDB as ddb
import utils as ut

Direction = gw.Direction

ahk = AHK()

def comparePos(pos1,pos2):
    return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])

offset = 5

starttime = time.monotonic()
step =None
pos = None
hintFound = 0

while True:
    time.sleep(1)
    try:    
        way,hint,nstep,hintimage,origin = gw.findBoard()
        start = gw.find_pos(origin)
        if start is None:
            continue
        if step is None:
            print("start")
    except Exception as e:
        continue
    if step == nstep:
        if start == pos:
            gw.clicNextStep()
            hintFound+=1
            print(f'${step}/${len(way)}')
            if step == len(way):
                gw.clickValider()
                hintfound = 0
                step = 0
            # cv.imshow("cropped", hintimage[step-1])
            # cv.waitKey(0)
        continue
    try:
        print(hint)
        print(way)
        print(step)
        stepnumber = len(way)
        print(f'start ${start}, hint ${hint} way ${way} step ${step} step number ${len(way)}')
        # print(origin,start)
        if nstep == 1: 
            isInHavreSac = start[0]==0 and start[1]==0
            if comparePos(origin,start) < 20 and not isInHavreSac :
                start = origin
                # ahk.click(x=1000,y=600)
            else:
                print('troplouin')
                continue
        step = nstep
        if hint[step-1] == '?':
            print('wtf')
        # if hint[step-1]:
        pos = ddb.get_hints(direction=way[step-1],position_x=start[0],position_y=start[1],hint=hint[step-1])
        hintm = ut.trouver_chaine_proche(hint[step-1])
        if pos is None and 'Phorreur' in hintm:
            print(way[step-1])
            to_go = None
            if way[step-1] == Direction.UP:
                to_go = (start[0],start[1]-10)
            if way[step-1] == Direction.DOWN:
                to_go = (start[0],start[1]+10)
            if way[step-1] == Direction.RIGHT:
                to_go = (start[0]+10,start[1])
            if way[step-1] == Direction.LEFT:
                to_go = (start[0]-10,start[1])
            gw.travelToPos(to_go)
            press_and_release('esc') # hold down the shift key
            time.sleep(0.1 - ((time.monotonic() - starttime) % 0.1))

            press_and_release('esc')
            pyautogui.click(x=95,y=15)  
            pyautogui.click(x=95,y=15)  
            ahk.key_down('z')

             # hold down the shift key
            while True:
                time.sleep(1)

                if gw.isThereAPhorreur():
                    ahk.click(x=1000,y=600)
                    time.sleep(0.2- ((time.monotonic() - starttime) % 0.2))
                    gw.clicNextStep()
                    # time.sleep(0.5 - ((time.monotonic() - starttime) % 0.5))
                    hintFound+=1
                    if step == len(way):
                        gw.clickValider()
                        hintfound = 0
                        step = 0
                    break

        # if pos is None:
        #     print(hint)
        #     start = (-start[0],start[1])
        #     pos = ddb.get_hints(direction=way[step-1],position_x=start[0],position_y=start[1],hint=hint[step-1])
        #     lastPos =start
        if pos:
            gw.travelToPos(pos)

    except Exception as e:
        continue
