from __future__ import print_function
from PIL import Image, ImageTk
import tkinter as tk
import threading
import cv2 as cv
from tkinter import ttk
from imutils.video import VideoStream

class PhotoBoothApp:
    def __init__(self, vs):
        self.vs = vs
        self.frame = None
        self.thread = None
        self.stopEvent = None

        self.root = tk.Tk()
        self.panel = None

        btn = ttk.Button(self.root, text='Snapshot!', command= None)
        btn.pack(side='bottom', fill= 'both', expand= 'yes', padx=10, pady=10)

        self.stopEvent = threading.Event()
        # self.thread= threading.Thread(target=self.videoLoop, args=()).start()

        self.root.wm_title("PhotoBooth")
        self.root.wm_protocol('Delete', self.onClose)

    def videoLoop(self):
        try:
            while not self.stopEvent.is_set():
                self.frame = self.vs.read()
                self.frame = cv.resize(self.frame, (640,480))
                image = cv.cvtColor(self.frame, cv.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                if self.panel is None:
                    self.panel = tk.Label(image=image)
                    self.panel.image = image
                    self.panel.pack(side='left', padx=10, pady=10)

                else:
                    self.panel.configure(image=image)
                    self.panel.image = image
        except RuntimeError:
            print('[INFOR] caught a RuntimeError')

    def onClose(self):
        print('[INFOR] closing....')
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()

vs = VideoStream(usePiCamera=0).start()

app = PhotoBoothApp(vs)
app.root.mainloop()

