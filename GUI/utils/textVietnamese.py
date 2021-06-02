import glob
def loadTXT(id, path='Data'):
    name = path +'/' + str(id) +'.config'
    text = ''
    with open(name, 'r+', encoding='utf_8') as stream:
        for line in stream.readlines():
            text += line
    stream.close()
    return text

def changeIm(path = 'Image'):
    import imutils
    import cv2 as cv
    import os
    for files in os.listdir(path):
        name = files.split('.')[0]
        img = cv.imread(path + '/' + files)
        img = imutils.resize(img, width= 200)
        cv.imwrite('Image1/' + name + '.jpg', img)
        print(name)
if __name__ == "__main__":
    changeIm()
