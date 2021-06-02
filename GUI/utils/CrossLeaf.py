import cv2 as cv
import numpy as np
import os
import glob
import imutils
from tkinter import filedialog as fd
import matplotlib.pyplot as plt
def changSquare(image):

    height, width = image.shape[:2] if len(image.shape) >2 else image.shape
    # print(image.shape)
    x = int(1.5*height) if height > width else int(1.5*width)
    square = np.ones((x, x), np.uint8)
    n = (255,255,255)
    
    if len(image.shape)>2:
        d1 = square * n[0]
        d2 = square * n[1]
        d3 = square * n[2]
        square = np.dstack((d1,d2, d3))
    else:
        square = square * n[0]
    square[int((x - height) / 2):x - int((x - height+1) / 2), int((x - width) / 2):x - int((x - width+1) / 2)] = image
    return square
def changeSquare2(image, x, y, w, h):
    xCenter = int(x + w/2)
    yCenter = int(y + h/2)
    # print(xCenter, yCenter)
    width = int(h / 2) if h > w else int(w / 2)
    height = int(h / 2) if h > w else int(w / 2)
    output = image[yCenter-height: yCenter + height, xCenter - width: xCenter + width]
    return output

def changSquare3(image):

    height, width = image.shape[:2] if len(image.shape) >2 else image.shape
    x = height if height > width else width
    square = np.ones((x, x), np.uint8)
    if len(image.shape)>2:
        d1 = square * 255
        d2 = square * 255
        d3 = square * 255
        square = np.dstack((d1,d2, d3))
    else:
        square = square * 255
    square[int((x - height) / 2):x - int((x - height+1) / 2), int((x - width) / 2):x - int((x - width+1) / 2)] = image
    return square

def markBinary(image):
    if (len(image.shape)>2):
        im = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    else:
        im = image
    ret, thresh1 = cv.threshold(im, 120, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
    ker = cv.getStructuringElement(cv.MORPH_ELLIPSE, (10, 10))
    bw1 = cv.dilate(thresh1, ker, iterations=3)
    bw2 = cv.erode(bw1, ker, iterations=4)
    bw = cv.bitwise_or(thresh1, bw2)
    return bw

def hsvNew(path):
    image = cv.imread(path)
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV).astype(np.float)
    h_new = (np.mod(hsv[:, :, 0] + 45, 180) / 180)
    v_new = 1 - (hsv[:, :, 2] / 255)
    hsv_new = h_new * 0.5 + v_new * 0.5
    hsvNew = np.uint8(255 * hsv_new / np.max(hsv_new))
    binary = markBinary(image)
    return image, hsvNew, binary

def New(path):
    image = cv.imread(path)
    image = imutils.resize(image, width= 768)
    binary = markBinary(image)
    return image, binary

def remove(image, binary):
    invert_binary = 255 - binary
    invert_binary = np.dstack((invert_binary, invert_binary, invert_binary))

    obj = cv.bitwise_and(image.copy(), image.copy(), mask=binary)
    objWhite= cv.bitwise_or(obj, invert_binary)
    return objWhite

def cross(image, binary):
    imageWhite= remove(image, binary)
    imageWhite = changSquare(imageWhite)
    leafBG = changSquare(image)
    leafBG1 = changSquare3(image)
    binary = markBinary(imageWhite)
    contours = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    if len(contours) > 0:
        contour = max(contours, key=cv.contourArea)
        [x, y, w, h] = cv.boundingRect(contour)
        leafBG = changeSquare2(leafBG, x, y, w, h )
        leafWhite = changeSquare2(imageWhite, x, y, w, h)
        return leafBG, leafBG1, leafWhite

def cross2(image, binary):
    imageWhite= remove(image, binary)
    imageWhite = changSquare(imageWhite)
    leafBG = changSquare(image)
    binary = changSquare(binary)
    contours = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    if len(contours) > 0:
        contour = max(contours, key=cv.contourArea)
        [x, y, w, h] = cv.boundingRect(contour)
        print([x, y, w, h])
        xCenter = int(x + w / 2)
        yCenter = int(y + h / 2)
        radian = int(h/2) if h > w else int(w/2)
        cv.circle(leafBG,(xCenter, yCenter), radian, (0,0,255), thickness= 5, )
        return leafBG

def file():
    # root = Tk()
    filenames = fd.askopenfilename(initialdir = " ",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    # print(root.filenames)
    # image = cv.imread(filenames, 1)
    image, binary = New(filenames)
    # out, out1 = cross(image, binary)
    out, out1, out2= cross(image, binary)
    cv.namedWindow("Out", cv.WINDOW_GUI_NORMAL)
    cv.imshow("Out", out1)
    cv.namedWindow("Out1", cv.WINDOW_GUI_NORMAL)
    cv.imshow("Out1", out2)
    cv.waitKey(0)
    cv.destroyAllWindows()
    # plt.imshow(out)
    # plt.show()
    # plt.imshow(binary)
    # plt.show()
def multifile():
    pathNewBG = r'D:\leaf\NewBG'
    pathNewWh = r'D:\leaf\NewWh'
    pathNew = r'D:\leaf\New'
    if not os.path.isdir(pathNewBG):
      os.makedirs(pathNewBG)
    if not os.path.isdir(pathNewWh):
      os.makedirs(pathNewWh)
    if not os.path.isdir(pathNew):
      os.makedirs(pathNew)
    with open('listLeaf.txt', 'r') as files:
        for line in files.readlines():
            try:
                pathImg = line.strip()
                name = pathImg.split('\\')
                image, binary = New(pathImg)
                print(name[-1])
                out, out1, out2 = cross(image, binary)
                out = imutils.resize(out, width=608)
                out1 = imutils.resize(out1, width=608)
                out2 = imutils.resize(out2, width=608)
                if not os.path.isdir(pathNewBG + '/' + name[-2]):
                    os.makedirs(pathNewBG + '/' + name[-2])
                if not os.path.isdir(pathNewWh + '/' + name[-2]):
                    os.makedirs(pathNewWh + '/' + name[-2])
                if not os.path.isdir(pathNew + '/' + name[-2]):
                    os.makedirs(pathNew + '/' + name[-2])
                cv.imwrite(pathNewBG + '/' + name[-2] + '/'+ name[-1], out)
                cv.imwrite(pathNewWh + '/' + name[-2] + '/'+ name[-1], out2)
                cv.imwrite(pathNew + '/' + name[-2] + '/' + name[-1], out1)
            except:
                pass

def multifile1():
    pathNew = r'D:\leaf\New2'
    if not os.path.isdir(pathNew):
      os.makedirs(pathNew)
    with open('listLeaf.txt', 'r') as files:
        for line in files.readlines():
            try:
                pathImg = line.strip()
                name = pathImg.split('\\')
                print(name)
                image = cv.imread(pathImg)
                img90 = imutils.rotate(image, 90)
                img180 = imutils.rotate(image, 180)
                img270 = imutils.rotate(image, 270)

                if not os.path.isdir(pathNew + '/' + name[-2]):
                    os.makedirs(pathNew + '/' + name[-2])
                cv.imwrite(pathNew + '/' + name[-2] + '/' + name[-1], image)
                cv.imwrite(pathNew + '/' + name[-2] + '/90-' + name[-1], img90)
                cv.imwrite(pathNew + '/' + name[-2] + '/180-' + name[-1], img180)
                cv.imwrite(pathNew + '/' + name[-2] + '/270-' + name[-1], img270)
            except:
                pass

if __name__ == '__main__':
    # file()
    # multifile()
    multifile1()