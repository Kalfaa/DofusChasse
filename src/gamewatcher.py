import cv2 as cv
import pyautogui
from paddleocr import PaddleOCR, draw_ocr
from enum import Enum
import re
import numpy as np
import typing
import time
import pyperclip as pc
from ahk import AHK
from keyboard import press_and_release,press
from ppocr.utils.logging import get_logger
import logging

logger = get_logger()
logger.setLevel(logging.ERROR)
lastPos = None

ocr = PaddleOCR(use_angle_cls=True, lang='fr')



Aright = cv.imread('../img/ArrowRight.PNG', cv.IMREAD_GRAYSCALE)
Aleft = cv.imread('../img/ArrowLeft.PNG', cv.IMREAD_GRAYSCALE)
ADown = cv.imread('../img/ArrowDown.PNG', cv.IMREAD_GRAYSCALE)
AUp = cv.imread('../img/ArrowUp.PNG', cv.IMREAD_GRAYSCALE)
template = cv.imread('../img/LINEPNG.PNG', cv.IMREAD_GRAYSCALE)
el = cv.imread('../img/valid.PNG', cv.IMREAD_GRAYSCALE)
encour = cv.imread('../img/encour.PNG', cv.IMREAD_GRAYSCALE)
butvalid = cv.imread('../img/butvalid.PNG', cv.IMREAD_GRAYSCALE)
phorreur = cv.imread('../img/Phorreur.PNG', cv.IMREAD_GRAYSCALE)
minus = cv.imread('../img/minus.PNG', cv.IMREAD_GRAYSCALE)

offset = 5
patternOrigin = r'\[(.*?)\]'

class Direction(Enum):
    LEFT=4
    RIGHT=0
    UP=6
    DOWN=2



def clickValider():
    img_s = np.array(pyautogui.screenshot())
    gray = cv.cvtColor(img_s , cv.COLOR_BGR2GRAY)
    img_s = cv.resize(gray ,(1920,1080))
    p = findMultipleTemplate(gray,butvalid,False)

    pyautogui.moveTo(p[0]['pt']+15,p[0]['pt1']+5, 0.2)
    pyautogui.click() 
    pyautogui.moveTo(1000,500, 0.2)
    
def clicNextStep():
    img_s = np.array(pyautogui.screenshot())
    gray = cv.cvtColor(img_s , cv.COLOR_BGR2GRAY)
    p = findMultipleTemplate(gray,encour,False)
    filtered = []
    for point in p:
        if point['pt'] <1640:
            continue
        filtered.append(point)
    filtered = sorted(filtered, key=lambda x: x['pt1'], reverse=True)
    filtered.pop()
    # print(filtered)
    pyautogui.moveTo(filtered[0]['pt'],filtered[0]['pt1'], 0.2)
    pyautogui.click() 
    pyautogui.moveTo(1000,500, 0.2)

def find_arrow(image):
        # image = cv.copyMakeBorder(image, 20, 20, 20, 20, cv.BORDER_CONSTANT, value=[0, 0, 0])
        # image = cv.threshold(image, 0, 255,cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
        # image = cv.bitwise_not(image)
        # print('arrow')
        # cv.imshow("cropped", image)
        # cv.waitKey(0)
        height, width = image.shape[:2]
        try:
            resultUp = cv.matchTemplate(image, AUp, cv.TM_CCOEFF_NORMED)
            min_valUp, max_valUp, min_locUp, max_locUp = cv.minMaxLoc(resultUp)

        except Exception:
            max_valUp = 0

        try:
            resultRight = cv.matchTemplate(image, Aright, cv.TM_CCOEFF_NORMED)
            min_valRight, max_valRight, min_locRight, max_locRight = cv.minMaxLoc(resultRight)
        except Exception:
            max_valRight = 0

        try:
            resultDown = cv.matchTemplate(image, ADown, cv.TM_CCOEFF_NORMED)
            min_valDown, max_valDown, min_locDown, max_locDown = cv.minMaxLoc(resultDown)

        except Exception:
            max_valDown = 0

        try:
            resultLeft = cv.matchTemplate(image, Aleft, cv.TM_CCOEFF_NORMED)
            min_valLeft, max_valLeft, min_locLeft, max_locLeft = cv.minMaxLoc(resultLeft)
        except Exception:
            max_valLeft = 0

        # resultRight = cv.matchTemplate(image, Aright, cv.TM_CCOEFF_NORMED)
        # resultDown = cv.matchTemplate(image, ADown, cv.TM_CCOEFF_NORMED)
        # resultLeft = cv.matchTemplate(image, Aleft, cv.TM_CCOEFF_NORMED)

        # min_valRight, max_valRight, min_locRight, max_locRight = cv.minMaxLoc(resultRight)
        # min_valDown, max_valDown, min_locDown, max_locDown = cv.minMaxLoc(resultDown)
        # min_valLeft, max_valLeft, min_locLeft, max_locLeft = cv.minMaxLoc(resultLeft)
        if max(max_valDown,max_valUp,max_valRight,max_valLeft) == 0:
            print('noarrow found')
        ##print("UP" +str(max_valUp))
        ##print("Down" + str(max_valDown))
        ##print("Right" + str(max_valRight))
        ##print("Left" + str(max_valLeft))
        ##print("Unkown" + str(max_valUNKNOWN))

        if max_valUp > max_valRight and max_valUp > max_valDown and max_valUp > max_valLeft:
            return Direction.UP

        if max_valLeft > max_valRight and max_valLeft > max_valDown and max_valLeft > max_valUp :
            return Direction.LEFT

        if max_valDown > max_valRight and max_valDown > max_valLeft and max_valDown > max_valUp :
            return Direction.DOWN

        if max_valRight > max_valDown and max_valRight > max_valLeft and max_valRight > max_valUp:
            return Direction.RIGHT


def findBoard():
    img_rgb = cv.cvtColor(np.array(pyautogui.screenshot(region=(1550,100,600,800))) , cv.COLOR_RGB2BGR)
    assert img_rgb is not None, "file could not be read, check with os.path.exists()"
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    assert template is not None, "file could not be read, check with os.path.exists()"
    w, h = template.shape[::-1]
    # cv.imshow("cropped", img_rgb)
    # cv.waitKey(0)
    result =findMultipleTemplate(img_gray,template)
    result2 =findMultipleTemplate(img_gray,el,False)
    # print(result2)
    result2[0]['pt1'] = result2[0]['pt1'] -10
    result.append(result2[0])
    # print('hint')
    # print(len(result)-1)
    # cv.imwrite('res.png',img_rgb)
    hint = []
    way = []
    hintimage = []
    origin = None
    for idx, x in enumerate(result):
            y = result[idx]["pt1"]
            if idx == len(result)-1:
                continue
            h = (result[idx+1]["pt1"])
            size = (h+offset)-(y+offset)
            a = img_gray[y+offset:h+offset, 58:370]
            # cv.imshow("cropped", a)
            # cv.waitKey(0)
            # print(size)
            if idx == 0:
                try:
                    text1 = ocr.ocr(a, cls=True)[0][0][1][0]
                    match = re.search(patternOrigin, text1)
                    tmpor = match.group(1).split(',')
                    origin = (int(tmpor[0]),int(tmpor[1]))
                except e :
                    pass
                continue
            hintimage.append(a)
            if size > 38 and size< 60:
                # print(size)
                crop_img = img_gray[y+offset:h-15, 67:255]
                # cv.imshow("cropped", crop_img)
                # cv.waitKey(0)
                gray = cv.threshold(crop_img, 0, 255,
                                    cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
                gray = cv.copyMakeBorder(gray, 20, 20, 20, 20, cv.BORDER_CONSTANT, value=[0, 0, 0])
                ##gray = cv.medianBlur(gray, 3)
                gray = cv.bitwise_not(gray)
                crop_img = gray
                # cv.imshow("cropped", crop_img)
                # cv.waitKey(0)
                text1 = ocr.ocr(crop_img, cls=True)[0][0][1][0]
                # print(text1)
                crop_img = img_gray[y+offset+20:h, 67:240]
                # cv.imshow("cropped", crop_img)
                # cv.waitKey(0)
                # cv.imshow("cropped", crop_img)
                
                text2 = ocr.ocr(crop_img, cls=True)[0][0][1][0]
                # print(text2)
                text = text1+' '+text2
            elif size > 60:
                crop_img = img_gray[y+offset:h-35, 58:255]
                # cv.imshow("cropped", crop_img)
                # cv.waitKey(0)
                gray = cv.threshold(crop_img, 0, 255,
                                    cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
                gray = cv.copyMakeBorder(gray, 20, 20, 20, 20, cv.BORDER_CONSTANT, value=[0, 0, 0])
                ##gray = cv.medianBlur(gray, 3)
                gray = cv.bitwise_not(gray)
                crop_img = gray

                text1 = ocr.ocr(crop_img, cls=True)[0][0][1][0]
                # print(text1)
                crop_img = img_gray[y+offset+20:h-15, 58:240]
                # cv.imshow("cropped", crop_img)
                # cv.waitKey(0)
                
                text2 = ocr.ocr(crop_img, cls=True)[0][0][1][0]

                crop_img = img_gray[y+offset+30:h, 58:240]
                # cv.imshow("cropped", crop_img)
                # cv.waitKey(0)
                
                text3 = ocr.ocr(crop_img, cls=True)[0][0][1][0]

                # print(text2)
                text = text1+' '+text2 + ''+ text3
            else:
                crop_img = img_gray[y+offset:h+offset, 58:260]

                # gray = cv.copyMakeBorder(crop_img, 20, 20, 20, 20, cv.BORDER_CONSTANT, value=[0, 0, 0])
                # gray = cv.threshold(gray, 0, 255,cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
                # gray = cv.bitwise_not(gray)
                crop_img = crop_img
                crop_img = img_gray[y+offset:h+offset, 58:260]
                # cv.imshow("cropped", crop_img)
                # cv.waitKey(0)
                text = getTextFromImage(crop_img)
                # print(text)
                if text is None or len(text)==0:
                    text ='?'

                    

                # text = pytesseract.image_to_string(crop_img)
            hint.append(text)
            # crop_img = img_rgb[y+offset:h+offset, 58:150]
            try:
                a = img_gray[y+offset:h+offset, 58:255]
                ar = find_arrow(a)
                # print(ar)
                way.append(ar)
            except Exception as e:
                print(e)
                # cv.imwrite('mtz.png',crop_img)
            # cv.imshow("cropped", crop_img)
            # cv.waitKey(0)
    step = 0
    for i in hint:
        # print(len(i))
        if len(i)>4:
            step+=1
    return way,hint,step,hintimage,origin



def travelToPos(pos:typing.Tuple[int,int]):
    text_to_copy = f"/travel {pos[0]} {pos[1]}"
    pc.copy(text_to_copy)
        
    time.sleep(0.3)
    press_and_release('tab')

    time.sleep(0.3)

    pyautogui.keyDown('ctrl')  # hold down the shift key
    pyautogui.press('v')     # press the left arrow key
    # # press the left arrow key
    pyautogui.keyUp('ctrl')
    time.sleep(0.3)

    press_and_release('enter')
    time.sleep(0.3)
    press_and_release('enter')

def isThereAPhorreur()->bool: 
        img_s = np.array(pyautogui.screenshot())
        gray = cv.cvtColor(img_s , cv.COLOR_BGR2GRAY)
        img_s = cv.resize(gray ,(1920,1080))
        res = findMultipleTemplate(img_s,phorreur,False,0.7)
        return len(res)>0

POS_PATTERN = r'(-?\d{1,2})\s*(.|,|;|:)\s*(-?\d{1,2})'

def find_pos(origin,lastPos=None):
    img_s = np.array(pyautogui.screenshot(region=(0,70,100,50)))

    gray = cv.cvtColor(img_s , cv.COLOR_BGR2GRAY)
    find_minus_x = len(findMultipleTemplate(gray[0:40,0:40],minus))
    results = ocr.ocr(gray, det=True, cls=False, rec=True)
    if results[0] is None:
        return None
    for (det_bbox, rec_str) in results[0]:
        strp= rec_str[0].replace('O','0')
        match = re.search(POS_PATTERN, strp)
        if match:
            # print('tamer')
            x, punct, y = match.groups()
            # print(x, y)
            # print(origin[0] - int(x))
            x = int(x)
            y = int(y)
            if lastPos is not None:
                if abs(origin[0] - int(x)) > 15:
                    x = -x
                if abs(lastPos[1] - int(y)) > 15:
                    # print(y)
                    y = -y
            if x > 0 and find_minus_x:
                x = -x
            return x, y
    return None


def remove_duplicates_by_key(data, key):
    """
    Supprime les doublons dans une liste de dictionnaires en se basant sur une clé donnée.

    :param data: Liste de dictionnaires
    :param key: Clé utilisée pour identifier les doublons
    :return: Liste de dictionnaires sans doublons
    """
    seen = set()
    unique_data = []
    pt = None
    for item in data:
        if item[key] not in seen:
            if pt is not None and -5 <pt - item[key] < 5:
                continue
            seen.add(item[key])
            pt = item[key]
            unique_data.append(item)
    return unique_data


def findMultipleTemplate(img,tpl,show=False,threshold = 0.7):
    w, h = tpl.shape[::-1]
    
    res = cv.matchTemplate(img,tpl,cv.TM_CCOEFF_NORMED)

    loc = np.where( res >= threshold)
    coord= []
    for pt in zip(*loc[::-1]):
        if show:
            cv.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
            cv.imshow("cropped", img)
            cv.waitKey(0)
            print({"pt":pt[0],"pt1":pt[1],"w":w,"h":h})
        coord.append({"pt":pt[0],"pt1":pt[1],"w":w,"h":h})
    if show:
        cv.imshow("cropped", img)
        cv.waitKey(0)
    result = remove_duplicates_by_key(coord, 'pt1')

    return result


def getTextFromImage(img):
    # cv.imshow("cropped", img)
    # cv.waitKey(0)
    results = ocr.ocr(img, det=True, cls=False, rec=True)
    # print(results)
    if results[0] is None:
        return ''
    for (det_bbox, rec_str) in results[0]:

        # print(det_bbox)
        # print(rec_str)
        return rec_str[0]