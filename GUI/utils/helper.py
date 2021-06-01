import cv2 as cv
import numpy as np
from PIL import Image, ImageTk
import imutils

FONT_LAGRE = ("Aller", 20, "bold italic")
FONT_REGULAR = ("Times", 14)
FONT_SMALL = ("Times", 10,"bold")
COLOR_RED = (31,0,178)
COLOR_GREEN = (43,189,91)
COLOR_YELLOW =(0,244,249)
COLOR_BLUE = (149,79,27)
COLOR_WHITE = (255,255,255)
COLOR_BLACK = (0,0,0)
COLOR_NAME = "spring green"
CODE_GREEN = "#00A06B"
CODE_BG = "#55DFAF"
CODE_BLACK = "#FFFFFF" 
CODE_WHITE = '#D5F5E3'

def changeShape(image):
    height, width = image.shape[:2] if len(image.shape) > 2 else image.shape
    # print(image.shap
    x = height if height > width else width
    square = np.ones((x, x), np.uint8)
    if len(image.shape) > 2:
        d1 = square * 255
        d2 = square * 255
        d3 = square * 255
        square = np.dstack((d1, d2, d3))
    else:
        square = square * 255
    square[int((x - height) / 2):x - int((x - height + 1) / 2),
    int((x - width) / 2):x - int((x - width + 1) / 2)] = image
    return square

def loadTXT(id, path='Data'):
    name = path +'/' + str(id) +'.txt'
    text = ''
    with open(name, 'r+', encoding='utf_8') as stream:
        for line in stream.readlines():
            # line = line.strip()
            text += line
    stream.close()
    return text
def loadImage(id, path='ImageData'):
    name = path + '/' + str(id) +'.jpg'
    img = ImageTk.PhotoImage(Image.open(name))
    return img
