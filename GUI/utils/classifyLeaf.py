from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import threading
import cv2 as cv
from tkinter import ttk
from imutils.video import VideoStream
from helper import *

class classifyLeaf(tk.Frame):

    def __init__(self, parent, controlling):
        tk.Frame.__init__(self, master=parent)
        tk.Frame.configure(self, bg=CODE_BG)
        # self.columnconfigure(0, weight=1)
        # self.rowconfigure(0, weight=1)
        # Camera Area
        self.cam = ttk.LabelFrame(self, text="Display",width=480, height=360)
        self.cam.grid(row=0, column=0, padx=10, pady=10, sticky="ewns")
        self.cam.rowconfigure(0, weight=1)
        self.cam.columnconfigure(0, weight=1)
        # Button Area
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.configure(bg=CODE_BG, height=360, width= 100)
        self.buttons_frame.grid(row=0, column=1, sticky="ne")

        btn_Video = ttk.Button(self.buttons_frame, text='Take Picture',
                               command=lambda: MainPage.loadVid(self))
        btn_Video.grid(row=0, column=0, padx=10, pady=10)

        btn_Data = ttk.Button(self.buttons_frame, text='Classification',
                              command=lambda: MainPage.loadData(self))
        btn_Data.grid(row=1, column=0, padx=10, pady=10)


        btn_Back = ttk.Button(self.buttons_frame, text="Back To Home",
                              command=lambda: controlling.show(BeginPage))
        btn_Back.grid(row=3, column=0, padx=10, pady=10)

        #Text Area
        self.text = ttk.LabelFrame(self, text="text", height=150)
        self.text.grid(row=1, column=0, padx=10, pady=10, sticky="ewns")
        self.text.rowconfigure(0, weight=1)
        self.text.columnconfigure(0, weight=1)
        # Value
        self.vs = None
        self.frame = None
        self.thread = None
        self.stopEvent = None
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=()).start()
        self.panel = None

    def videoLoop(self):
        self.vs = VideoStream(usePiCamera=0).start()
        try:
            while not self.stopEvent.is_set():
                self.frame = self.vs.read()
                self.frame = cv.resize(self.frame, (480,360))
                image = cv.cvtColor(self.frame, cv.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                if self.panel is None:
                    self.panel = tk.Label(master=self.cam, image=image)
                    self.panel.image = image
                    self.panel.pack(side='left', padx=10, pady=10)

                else:
                    self.panel.configure(image=image)
                    self.panel.image = image
        except RuntimeError:
            print('[INFOR] caught a RuntimeError')

