import tkinter as tk
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from enum import Enum
import requests
from paddleocr import PaddleOCR, draw_ocr
from unidecode import unidecode
import pyautogui
from ppocr.utils.logging import get_logger # type: ignore
import  time
import logging
import re
from keyboard import press_and_release,press
import pyperclip as pc
import win32com.client as win
import win32gui
import win32process
from ahk import AHK
import gamewatcher as gw
import DofusDB as ddb
import utils as ut
from threading import Thread

running = False
token_default = '03AFcWeA6iVVcyc97jIGreGqubFfVWwHGzGEbmnn1wD4bA0zWqDcWqeOdcXz-xBdKdAfqqp344LH1iGtWKHeBdraOpPKLNvTdYzyyGIHACYVEhzbyu-A6k77_ws-a2n45Rw4tLTHTiIdrcwGC2Gd5y0Mtg93rvx7DSA5UbO1Ll0z3MtlULHjHSiMlcgfS08bW7ivPOLU7yW__9zPnAQqPtzPhLvoijQcyTVU-hJw255AhP4p9RlZvMV2gBCQkYG3Hm3qwNtd8_oj4ufP4Ts4oSppFuAcH0M_PhP1Jkh1uigAfD1lNm4Zb7FCpyPLQLg72RfHwZFJvwxjtAWZjcIG1JcQEJora3xIv-OPsJiSstkiHbA-AKPhrSS8JOH5ApTss5SM08hGhgK4HFOIkr9TSs0KZ8ecMVvUNHnYwH4Se3SJhmfGZUN2voTlu1ejq61JAaIgoZilWhSWQ0N9KwSQ6KAG6Nu4_l0_kMHZAAm53lfLbqJ-V-RIA8ejbyRr_D47Q8oK9iCDfbqn6VTyEb3zBg5YH-pn7KfixGh3Ul2qbSHK52E62pc548seP2wvCZCj6B4_C9wwA_0Sgp5hnTLGArxIWySlXSF9J-4nKfwsmvEN67ebhsBYapUdxPRwvZ1dVSjK6AFPCBbV5BPbR-KItWtwMh177-CnEefN6lcT9Ssdsr7g_Dr--04e9fQF5WqymLEOFPbf9Q9V2-7EWpSQFjdrE8UpCO43qpthw1j4oc9JdfWuOaYVB5UxLg2rOHz7Jll3huJRJlkUfZ8X_VkjXqRAlHO_jcCg-2jKD3tmPZ6KANDMW94nHK1vuU5hFtIbMsGV3qrLPLKPBOmJo_JfGGgGItNEw1P5CPdR3uI0rqnXDIdzI79g3xX8xKDfz4df3IKmzAWTXnTzIspDFz4eeCpNJJd2-lzAAqNGqPtCLV5yxOR2FQcbc-fRwHZ_nZIes4cZfEaexeXg-J3TypwkPZZd-yi6ENxa6to1V9duCVTgTHZL1kTOP_zVYZm0J1J8By68Hbtm86EPvFBdMGgWQnRKAD2qYNqkuxSx1YcfY_-Nl7dBb1OSqvnqWKjMVxk8E2wlFSkWlNj0wQdhUXsEOjbjWr2xmNkKxv_FuDJdvCjVIdRcbHq2p1yfXxfH-N-oCala3rCoskzbJCF7eMEdXGRXijevZ_qPLiVnZlkWjVUIOdvITcEB9dwUvckeolpBbekua4QmPdwVoNqg4bihbyA8avh82jCOhathqUSZPw1CKIU5wlVp4XHIV0ymHYd_vRR59AXnHUaErGc9tiytB51nvZ1eDTi1gbix1hf4CsB6jezeZ87OI5esA6bBY_X96I-dn_FGjprmUyXFNm11aJvo7cbArbFFkyXkcCD0i7mINQr7ocEFrzRYSMLbkN8kSEnqjXaj6hipR5p_aZ2QK5capGYkyIEzCFRTad0nLEAuFWcYQ2tdIggoptJvI271YX31leOh4g2vuYOu5TPzK-1X5c-xUQRFMhRe_Wvm29XrtWC2iW4NCoidvCEr6VhcXSU537qh9Xcx4VBIz_8YY63qkUFOYx_Z0cLyzjHU0OQjXbQXR5_DdkwFcAmw1Q5-NZNgxHM2gWjHtVQFTyz77PpHtd5sI5RGNGH04BktM9X7sQo6BPsS5v68nP-741G4ZxrMEWkvIgosOEP4HLwfq61hWaAN973YJiEwuD_0xPmHcmn-BYyJu0F9RpCXIuMwmtrJyxFBO4zZNmI_AG1CSgpFPNFmgz3-HQXWV0Cs69TyZUzoqCJbRySBdw08_fR3zOHCAJzeAOkOLGf8GsWqn9b9Fc1pIFCA9mxbMtoa60zIv9e9A2KOGiA5VORDO4433oo0LdBBLYYaL0nQA8Rp7B08XDVNT5lJlzMHNoQgkhuyw6XrWiEcm9e28UFFYUkaj8PYFJB9bgbMusSLn1rMBIqDqPwSFwk9Eb-MiStWeFvJOUwyYXFo7iqHBU9QWTDbDbJZj98xuHByKhVa6l_cfRskx-kKnAZ-yyhzJTL7Mm81lIBp-ZpnEcjUNLgaJR_XVPFlGoh7talZM3r7KWT0QHXp4lW8JqZn8cuw1T20ESr1Kpccel4l1aEwTcmzYx1XGfxVnOTXEaeFo3K_cxAnpuB8UeJnLN7S2Fm0Er3tv2jYiQfofTDOCWz5IE3eKAd6kUr_6AXFZFd_5p'
thread = None

def chasse():
    Direction = gw.Direction

    ahk = AHK()

    def comparePos(pos1,pos2):
        return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])

    offset = 5
    global running, token
    starttime = time.monotonic()
    step =None
    pos = None
    hintFound = 0
    print("before running")
    while running:
        print("running")
        time.sleep(1)
        try:    
            way,hint,nstep,hintimage,origin = gw.findBoard()
            start = gw.find_pos(origin)
            # print(start)
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
            pos = ddb.get_hints(direction=way[step-1],position_x=start[0],position_y=start[1],hint=hint[step-1],token=token)
            hintm = ut.trouver_chaine_proche(hint[step-1])
            print('go to',pos)
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
            if pos:
                gw.travelToPos(pos)

        except Exception as e:
            continue

def easy_thread():
    while running:
        print("allo")
        time.sleep(1)

def toggle_task():
    """Lance ou arrête la tâche de fond."""
    global running, thread
    running = not running
    if running:
        thread = Thread(target = chasse)
        thread.start()
        toggle_button.config(text="Arrêter la chasse")
        time.sleep(1)
          # Démarre la tâche de fond
    else:
        toggle_button.config(text="Lancer la chasse")
        if thread:
            thread.join()
            thread = None

def on_submit():
    """Callback exécutée lors de la soumission de l'entrée."""
    print(f"Utilisateur a entré : {token.get()}")

root = tk.Tk()
root.title("Fenêtre avec tâche de fond")

label = tk.Label(root, text="Entrez quelque chose et appuyez sur Soumettre :")
label.pack(pady=10)

token = tk.StringVar(value=token_default)
entry = tk.Entry(root, textvariable=token, width=40)
entry.pack(pady=10)

submit_button = tk.Button(root, text="Soumettre", command=on_submit)
submit_button.pack(pady=10)

toggle_button = tk.Button(root, text="Lancer la chasse", command=toggle_task)
toggle_button.pack(pady=10)

# Lancement de la boucle principale de Tkinter
root.mainloop()

