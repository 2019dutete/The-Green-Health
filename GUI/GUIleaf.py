import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import cv2 as cv
from utils.VideoStream import VideoStream
from utils.helper import *
from tkinter import filedialog as fd
import imutils
from tkinter import messagebox
#from keras.models import load_model

class leafApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, string= 'ETE GreenHealth')
        self._frame = None
        self.switch_frame(beginPage)

    def __del__(self):
        self.quit()
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(side='top', fill= 'both', expand = True)
        self._frame.grid_rowconfigure(0, weight=1)
        self._frame.grid_columnconfigure(0, weight=1)

class beginPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, master=parent)
        tk.Frame.configure(self, bg=CODE_WHITE)

        render1 = ImageTk.PhotoImage(Image.open('logo/LogoKhoa1.png'))
        img1 = tk.Label(self, image=render1, bg=CODE_WHITE)
        img1.image = render1
        img1.pack()
        tk.Label(self, text="Danang Universtity of Technology\n Electronic and Telecommunication Engineering",
                 bg=CODE_WHITE,
                 font=FONT_REGULAR).pack(anchor=tk.CENTER, padx=15, pady=10)

        render = ImageTk.PhotoImage(Image.open('logo/leaf6.png'))
        img = tk.Label(self, image=render, bg=CODE_WHITE)
        img.image = render
        img.pack()
        buttonMain = ttk.Button(self,
                                text="Main Program",
                                command=lambda: parent.switch_frame(classifyLeaf))
        buttonMain.pack(anchor=tk.CENTER, padx=10, pady=10)

        buttonAbout = ttk.Button(self,
                                 text="About",
                                 command=lambda: parent.switch_frame(InforPage))
        buttonAbout.pack(anchor=tk.CENTER, padx=10, pady=10)

        buttonExit = ttk.Button(self, text="Exit",command=quit)
        buttonExit.pack(anchor=tk.CENTER, padx=10, pady=10)
class InforPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, master=parent)
        tk.Frame.configure(self, bg=CODE_WHITE)
        tk.Label(self, bg=CODE_WHITE, text="Đề tài cuộc thi NCKH", font=FONT_REGULAR).pack(padx=10,pady=15)
        tk.Label(self, bg=CODE_WHITE, text="-----***-----", font=FONT_REGULAR).pack()
        tk.Label(self, bg=CODE_WHITE, text="Đề tài", font=FONT_SMALL).pack(padx=10, pady=15)
        tk.Label(self, bg=CODE_WHITE, text="DOCTOR LEAF \n Ứng dụng nhận dạng \nvà phân loại cây thuốc Nam",
				 font=FONT_LAGRE).pack(anchor= tk.CENTER, padx=10,pady=15)
        tk.Label(self, bg=CODE_WHITE, text="GVHD: Ths Hoàng Lê Uyên Thục", font=FONT_REGULAR).pack(padx=10, pady=15)
        # tk.Label(self, bg=CODE_WHITE, text="Sinh viên thực hiện:", font=FONT_REGULAR).pack(padx=10, pady=15)
        # tk.Label(self, bg=CODE_WHITE, text="Nguyễn Thành Long  15DT2", font=FONT_REGULAR).pack(padx=10, pady=15)
        # tk.Label(self, bg=CODE_WHITE, text="Nguyễn Đăng Hoàng 15DT1", font=FONT_REGULAR).pack(padx=10, pady=15)
        tk.Label(self, bg=CODE_WHITE, text="Cảm ơn đã xem", font=FONT_REGULAR).pack(side='bottom', padx=10, pady=15)
        button = ttk.Button(self,
							text="Back to home",
							command=lambda: parent.switch_frame(beginPage))
        button.pack(side='bottom', padx=10, pady=15)

class classifyLeaf(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, master=parent)
        tk.Frame.configure(self, bg=CODE_WHITE)
        self.count = 0
        # Camera Area
        self.cam = ttk.LabelFrame(self, text="Display", width=480, height=360)
        self.cam.grid(row=0, column=0, padx=10, pady=10, sticky="ewns")
        self.cam.rowconfigure(0, weight=1)
        self.cam.columnconfigure(0, weight=1)
        # Button Area
        buttons_frame = tk.Frame(self)
        buttons_frame.configure(bg=CODE_WHITE, height=360, width=100)
        buttons_frame.grid(row=0, column=1, sticky="ne")
        self.checkVar = tk.IntVar()
        self.checkVar.set(0)
        checkCam = tk.Checkbutton(buttons_frame, text='Using camera',
                                  variable=self.checkVar, onvalue=1,
                                  offvalue=0, bg=CODE_WHITE,
                                  command= self.getCheck)
        checkCam.grid(row=0, column=0, padx=10, pady=10)
        self.shot = ttk.Button(buttons_frame, text='Get Info',
                             command=self.snapShoot)
        self.shot.grid(row=1, column=0, padx=10, pady=10)
        
        btn_Img = ttk.Button(buttons_frame, text='Get Picture',command=self.getImage)
        btn_Img.grid(row=2, column=0, padx=10, pady=10)
        btn_Classify = ttk.Button(buttons_frame, text='Classification', command=self.classify)
        btn_Classify.grid(row=3, column=0, padx=10, pady=10)
        btn_Back = ttk.Button(buttons_frame, text="Back To Home", command=lambda: parent.switch_frame(beginPage))
        btn_Back.grid(row=4, column=0, padx=10, pady=10)
        # Text Area
        self.text = ttk.LabelFrame(self, text="text", height=200, width= 200)
        self.text.grid(row=1, column=0, padx=10, pady=10, sticky="ewns")
        self.text.rowconfigure(0, weight=1)
        self.text.columnconfigure(0, weight=1)
        self.scrollbar = ttk.Scrollbar(self.text)
        self.scrollbar.pack(side = tk.RIGHT, fill='y')
        # Value
        self.vs = None
        self.frame = None
        self.thread = None
        self.stopEvent = None
        self.panel = None
        self.info = None
        self.info1 = None

        self.net = cv.dnn.readNetFromDarknet("model/yolov3-tiny-leaf.cfg", "model/yolov3-tiny-leaf_8000.weights")
        self.classes = []
        with open("model/yolo.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        layer_names = self.net.getLayerNames()
        self.output_layers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        self.ID = -1
        self.conf = 0

    def __del__(self):
        self.stopEvent.set()
        self.vs.stop()
        self.panel.image = None

    def getCheck(self):
        if self.checkVar.get() == 1:
            self.stopEvent = threading.Event()
            self.vs = VideoStream(src=0, resolution=(608, 608)).start()
            self.thread = threading.Thread(target=self.videoLoop2, args=()).start()

        elif self.checkVar.get() == 0:
            print('[INFOR] closing....')
            self.stopEvent.set()
            self.vs.stop()
            self.panel.image = None

    # def videoLoop(self):
    #     try:
    #         while not self.stopEvent.is_set():
    #             self.frame = self.vs.read()
    #             image = imutils.resize(self.frame, width=480)
    #             image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    #             image = Image.fromarray(image)
    #             image = ImageTk.PhotoImage(image)
    #             if self.panel is None:
    #                 self.panel = tk.Label(self.cam, image=image)
    #                 self.panel.image = image
    #                 self.panel.pack(side='left', fill='both')
    #             else:
    #                 self.panel.configure(image= image)
    #                 self.panel.image = image
    #     except RuntimeError:
    #         print('[INFO] caught a RuntimeError')

    def videoLoop2(self):
        try:
            while not self.stopEvent.is_set():
                self.frame = self.vs.read()
                image = imutils.resize(self.frame, width=416)
                image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
                image = changeShape(image)
                height, width = image.shape[:2]
                blob = cv.dnn.blobFromImage(image, 0.00392,
                                            (416, 416), (0,0,0),
                                            False, crop=False)
                self.net.setInput(blob)
                outs = self.net.forward(self.output_layers)
                class_ids = []
                confidences = []
                boxes = []
                for out in outs:
                    for detection in out:
                        scores = detection[5:]
                        class_id = np.argmax(scores)
                        confidence = scores[class_id]
                        if confidence > 0.5:
                            # Object detected
                            center_x = int(detection[0] * width)
                            center_y = int(detection[1] * height)
                            w = int(detection[2] * width)
                            h = int(detection[3] * height)
                            # Rectangle coordinates
                            x = int(center_x - w / 2)
                            y = int(center_y - h / 2)
                            boxes.append([x, y, w, h])
                            confidences.append(float(confidence))
                            class_ids.append(class_id)
                indexes = cv.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

                for i in range(len(boxes)):
                    if i in indexes:
                        x, y, w, h = boxes[i]
                        cv.rectangle(image, (x, y), (x + w, y + h), COLOR_BLUE, 2)
                        text = "{}: {:.2f}%".format(str(self.classes[class_ids[i]]), confidences[i] * 100)
                        print(text)
                        # cv.putText(image, text, (int(x), int(y)), FONT_SMALL, 0.5, COLOR_BLUE, 1)
                        # image = cv.resize(image, (480,480))
                        self.ID = class_ids[i]
                        self.conf = confidences[i]
                self.img = image.copy()
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                if self.panel is None:
                    self.panel = tk.Label(self.cam, image=image)
                    self.panel.image = image
                    self.panel.pack(side='left', fill='both')
                else:
                    self.panel.configure(image= image)
                    self.panel.image = image
        except:
            print('[INFO] caught a RuntimeError')


    def getImage(self):
        pathImage = fd.askopenfilename(initialdir="", title="Select file",
                                          filetypes=(("jpg files", "*.jpg"),
                                                     ('JPG files', '*.JPG'),
                                                     ("all files", "*.*")))
        try:
            self.frame = cv.imread(pathImage)
            self.imgTest = self.frame.copy()
            if self.frame.shape[0]> self.frame.shape[1]:
                image = imutils.resize(self.frame, height=416)
            else:
                image = imutils.resize(self.frame, width= 416)
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)
            if self.panel is None:
                self.panel = tk.Label(self.cam, image=image)
                self.panel.image = image
                self.panel.pack(side='left', fill='both')
            else:
                self.panel.configure(image=image)
                self.panel.image = image
        except RuntimeError:
            print('[INFO] caught a runtimeError')

    def snapShoot(self):
        if self.checkVar.get() ==1:
            # self.vs.stop()
            # image = self.img
            # image = Image.fromarray(image)
            # image = ImageTk.PhotoImage(image)
            # if self.panel is None:
            #     self.panel = tk.Label(self.cam, image=image)
            #     self.panel.image = image
            #     self.panel.pack(side='left', fill='both')
            # else:
            #     self.panel.configure(image=image)
            #     self.panel.image = image
            self.putText(self.ID+1, self.conf)
            self.shot.config(text='Continue')
            

        else:
            messagebox.showerror(title= "ERROR", message="Camera chưa được bật")
        return

    def continueVideo(self):
        # self.vs.start()
        self.thread = threading.Thread(target=self.videoLoop2, args=()).start()
        return
    """
    def loadModel(self, pathfile):
        print('[INFO]Loading Model...')
        model = load_model(pathfile)
        print('[INFO]Loaded Model')
        return model
    """
    def putText(self, id = -1, conf= 0):
        try:
            confident = 'Độ chính xác: {0:.2f}%'.format(conf*100)
            text = loadTXT(id)
            info = confident +'\n' + text
            img = loadImage(id)
        except:
            info = "Vui Lòng thử lại."
            img = None
        
        if self.info is None and self.info1 is None:
            self.info = tk.Label(self.text, text=info, wraplength= 500, justify= 'left')
            self.info.info = info
            self.info.pack(side='left', fill='both')
            self.info1 = tk.Label(self.text, image=img)
            self.info1.img = img
            self.info1.pack(side='right')

        else:
            self.info.configure(text = info)
            self.info.info = info
            self.info1.configure(image=img)
            self.info1.img = img
        

    def classify(self):
        image = self.imgTest
        img = changeShape(image)
        img = cv.resize(img, (416, 416))
        height, width = img.shape[:2]
        blob = cv.dnn.blobFromImage(img, 0.00392,
                                    (416, 416), (0, 0, 0),
                                    False, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        indexes = cv.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                cv.rectangle(image, (x, y), (x + w, y + h), COLOR_BLUE, 2)
                text = "{}: {:.2f}%".format(str(self.classes[class_ids[i]]), confidences[i] * 100)
                print(text)
                # cv.putText(image, text, (int(x), int(y)), FONT_SMALL, 0.5, COLOR_BLUE, 1)
                # image = cv.resize(image, (480,480))
                label = class_ids[i]
                conf = confidences[i]
                self.putText(label+1, conf)


if __name__ == '__main__':
    app = leafApp()
    app.mainloop()