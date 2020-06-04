import json
from tkinter import *
from tkinter.ttk import Treeview

import cv2 as cv
import numpy as np
import pyautogui as pyautogui
import pytesseract
import requests

from game.GameState import GameState
from game.Line import Line
from game.board import Board
from game.gamewatcher import GameWatcher
global game
def setup():
    pytesseract.pytesseract.tesseract_cmd = r'F:\Tesseract-OCR\tesseract.exe'
    board = [cv.imread('../img/board.png', cv.COLOR_RGB2BGR),cv.imread('../img/LittleSizeBoard.png', cv.COLOR_RGB2BGR),cv.imread('../img/1HintBoard.png', cv.COLOR_RGB2BGR),cv.imread('../img/5HintBoard.png', cv.COLOR_RGB2BGR),cv.imread('../img/2Hint.png', cv.COLOR_RGB2BGR)]
    return board

def init_board():
    global board
    arrow = [cv.imread('../img/UP.png', cv.COLOR_RGB2BGR),cv.imread('../img/ArrowRight.png', cv.COLOR_RGB2BGR),cv.imread('../img/ArrowDown.png', cv.COLOR_RGB2BGR),cv.imread('../img/ArrowLeft.png', cv.COLOR_RGB2BGR),cv.imread('../img/UNKOWN.png', cv.COLOR_RGB2BGR)]
    board = Board(board_sprite, arrow,tableau)
    ##board.printMyState()
    print(board.lastHintKnown())



board_sprite = setup()
while 1:
    break
root = Tk()
root.geometry('1000x600')

b = Button(root,text="Zango",command=init_board)


def change_pos():
    global board
    if X.get()!= '' and Y.get()!= '':
        try:
            x = int(X.get())
            y = int(Y.get())
            board.pos_list[-1] =(x,y)
            X2.delete(0, END)
            Y2.delete(0, END)
        except Exception:
            print("Wrong pos")
            return


c = Button(root,text="POS",command=change_pos)
c.pack(side=RIGHT)

def next_step():
    global board
    if X.get()!= '' and Y.get()!= '':
        try:
            x = int(X.get())
            y = int(Y.get())
            board.next_step(x, y)
            X2.delete(0, END)
            Y2.delete(0, END)
        except Exception:
            print("Wrong pos")
            return
    else:
        board.next_step()
    X2.delete(0, END)
    Y2.delete(0, END)
a = Button(root,text="Next",command=next_step)
a.pack()
b.pack(side=BOTTOM)
X = StringVar()
Y = StringVar()
X1 = Label(root, text="X")
X1.pack( side = LEFT)
X2 = Entry(root, bd =5,textvariable=X)
X2.pack(side = LEFT)


Y1 = Label(root, text="Y")
Y1.pack( side = LEFT)
Y2 = Entry(root, bd =5,textvariable=Y)
Y2.pack(side = LEFT)

tableau = Treeview(root, columns=('Indice', 'Position','Direction'))

tableau.heading('Indice', text='Indice')

tableau.heading('Position', text='Position')

tableau.heading('Direction', text='Direction')

tableau['show'] = 'headings' # sans ceci, il y avait une colonne vide à gauche qui a pour rôle d'afficher le paramètre "text" qui peut être spécifié lors du insert

tableau.pack(padx = 10, pady = (0, 10))


root.mainloop()
