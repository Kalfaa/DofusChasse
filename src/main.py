from tkinter import *
from tkinter.ttk import Treeview

import cv2 as cv
import pytesseract
from pynput import keyboard

from board import Board

global game
def setup():
    pytesseract.pytesseract.tesseract_cmd = r'F:\Tesseract-OCR\tesseract.exe'
    board = [cv.imread('../img/board.png', cv.COLOR_RGB2BGR),cv.imread('../img/LittleSizeBoard.png', cv.COLOR_RGB2BGR),cv.imread('../img/1HintBoard.png', cv.COLOR_RGB2BGR),cv.imread('../img/5HintBoard.png', cv.COLOR_RGB2BGR),cv.imread('../img/2Hint.png', cv.COLOR_RGB2BGR),cv.imread('../img/3Hint.png', cv.COLOR_RGB2BGR)]
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


def getpos():
    global board
    pos=board.old_find_pos()
    X.set(pos[0])
    Y.set(pos[1])


c = Button(root,text="POS",command=getpos)
c.pack(side=RIGHT)


def setpos():
        global board
        try:
            x = int(X.get())
            y = int(Y.get())
            board.pos = (x,y)
            X2.delete(0, END)
            Y2.delete(0, END)
        except Exception:
            print("Wrong pos")
            return


d = Button(root,text="BROKEN",command=setpos)
d.pack(side=LEFT)

def next_step():
    global board
    if X.get()!= '' and Y.get()!= '':
            x = int(X.get())
            y = int(Y.get())
            board.next_step(x, y)
            X2.delete(0, END)
            Y2.delete(0, END)
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

tableau['show'] = 'headings' # sans ceci, il y avait une colonne vide ?? gauche qui a pour r??le d'afficher le param??tre "text" qui peut ??tre sp??cifi?? lors du insert

tableau.pack(padx = 10, pady = (0, 10))


def on_key_release(key):
    if str(key) == "Key.page_up":
        ##try:
            next_step()
        ##except Exception as e:
            ##print(e)

with keyboard.Listener(on_release = on_key_release) as listener:
    root.mainloop()
    listener.join()
