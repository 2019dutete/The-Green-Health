import cv2 as cv
import numpy as np
import os
import glob
import imutils
from tkinter import filedialog as fd
import matplotlib.pyplot as plt
import cv2 as cv

def changSquare3(image):

    height, width = image.shape[:2] if len(image.shape) >2 else image.shape
    x = height if height > width else width
    square = cv.resize(image, (x,x))
    square = np.mean(square)
    # square[int((x - height) / 2):x - int((x - height+1) / 2), int((x - width) / 2):x - int((x - width+1) / 2)] = image
    return square
def remove(image, binary):
    invert_binary = 255 - binary
    invert_binary = np.dstack((invert_binary, invert_binary, invert_binary))

    obj = cv.bitwise_and(image.copy(), image.copy(), mask=binary)
    objWhite= cv.bitwise_or(obj, invert_binary)
    return objWhite
# def cross(image, binary):
#     imageWhite= remove(image, binary)
#     imageWhite = changSquare(imageWhite)
#     leafBG = changSquare(image)
#     leafBG1 = changSquare3(image)
#     binary = markBinary(imageWhite)
#     contours = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
#     contours = imutils.grab_contours(contours)
#     if len(contours) > 0:
#         contour = max(contours, key=cv.contourArea)
#         [x, y, w, h] = cv.boundingRect(contour)
#         leafBG = changeSquare2(leafBG, x, y, w, h )
#         leafWhite = changeSquare2(imageWhite, x, y, w, h)
#         return leafBG, leafBG1, leafWhite

def New(path):
    image = cv.imread(path)
    image = imutils.resize(image, width= 768)
    return image

def file():
    filenames = fd.askopenfilename(initialdir = " ",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    image = New(filenames)
    out1 = changSquare3(image)

    # cv.namedWindow("Out", cv.WINDOW_GUI_NORMAL)
    # cv.imshow("Out", out2)
    #
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    plt.imshow(out1)
    plt.show()

if __name__ == '__main__':
    file()