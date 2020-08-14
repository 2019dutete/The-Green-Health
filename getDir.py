import numpy as np 
import os 
from tkinter import filedialog as fd
from tkinter import *

root = Tk()
root.direction = fd.askdirectory(title="Chon duong dan chua tap thu muc muon tao")
saveFile = os.path.join(root.direction, 'listLeaf.txt')
with open(saveFile, 'w+') as save:
    for files in os.listdir(root.direction):
        fullPath = os.path.join(root.direction, files)
        if not fullPath.endswith(".txt"):
            for file in os.listdir(fullPath):
                if not file.endswith('.rar'):
                    pathFolder = os.path.join(fullPath, file)
                    print(pathFolder)
                    save.write(pathFolder + '\n')


