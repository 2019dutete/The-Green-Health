import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox

from PIL import Image, ImageTk
import threading
import cv2 as cv
from imutils.video import VideoStream
from helper import *

class LeafApp(tk.Tk):

	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		tk.Tk.wm_title(self, string='DOCTOR LEAF')
		tk.Tk.geometry(self, newGeometry= "640x640+10+10")
		gui = tk.Frame(self)
		gui.pack(side='top', fill= 'both', expand = True)
		gui.grid_rowconfigure(0, weight=1)
		gui.grid_columnconfigure(0, weight=1)

		self.frames = {}
		for func in (BeginPage, InforPage, classifyLeaf):
			page = func(parent=gui, controlling=self)
			self.frames[func] = page
			page.grid(row=0, column=0, sticky= 'nsew')

		self.show(BeginPage)

	def __del__(self):
		self.quit()

	def show(self, listPage):
		frame = self.frames[listPage]
		frame.tkraise()

class BeginPage(tk.Frame):

	def __init__(self, parent, controlling):
		tk.Frame.__init__(self, master= parent)
		tk.Frame.configure(self, bg=CODE_BG)
		tk.Label(self, text="Danang Universtity of Technology\n Electronic and Telecommunication Engineering",
				 bg=CODE_BG,
				 font=FONT_REGULAR).pack(anchor=tk.CENTER, padx=15, pady=20)

		render = ImageTk.PhotoImage(Image.open('leaf1.png'))
		img = tk.Label(self, image=render, bg=CODE_BG)
		img.image = render
		img.pack()
		buttonMain = ttk.Button(self,
							 text="Main Program",
							 command= lambda : controlling.show(classifyLeaf))
		buttonMain.pack(anchor=tk.CENTER, padx=20, pady=20)

		buttonAbout = ttk.Button(self,
							 text="About",
							 command=lambda: controlling.show(InforPage))
		buttonAbout.pack(anchor=tk.CENTER, padx=20, pady=20)

		buttonExit = ttk.Button(self, text="Exit", command= quit)
		buttonExit.pack(anchor= tk.CENTER, padx = 20, pady = 20)

		info = tk.Label(self, text="Copyright (Leaf team) Nguyen Thanh Long, Nguyen Dang Hoang",
				 bg=CODE_BG,
				 font=FONT_SMALL,
				 fg=CODE_BLACK)
		info.pack(anchor=tk.CENTER, side='bottom', fill='both', padx=10, pady=10)

class InforPage(tk.Frame):

	def __init__(self, parent, controlling):
		tk.Frame.__init__(self, master=parent)
		tk.Frame.configure(self, bg=CODE_BG)
		tk.Label(self, bg=CODE_BG, text="Đề tài cuộc thi NCKH", font=FONT_REGULAR).pack(padx=10,pady=15)
		tk.Label(self, bg=CODE_BG, text="-----***-----", font=FONT_REGULAR).pack()
		tk.Label(self, bg=CODE_BG, text="Đề tài", font=FONT_SMALL).pack(padx=10, pady=15)
		tk.Label(self, bg=CODE_BG, text="DOCTOR LEAF \n Ứng dụng nhận dạng \nvà phân loại cây thuốc Nam",
				 font=FONT_LAGRE).pack(anchor= tk.CENTER, padx=10,pady=15)
		tk.Label(self, bg=CODE_BG, text="GVHD: Ths Hoàng Lê Uyên Thục", font=FONT_REGULAR).pack(padx=10, pady=15)
		tk.Label(self, bg=CODE_BG, text="Sinh viên thực hiện:", font=FONT_REGULAR).pack(padx=10, pady=15)
		tk.Label(self, bg=CODE_BG, text="Nguyễn Thành Long  15DT2", font=FONT_REGULAR).pack(padx=10, pady=15)
		tk.Label(self, bg=CODE_BG, text="Nguyễn Đăng Hoàng 15DT1", font=FONT_REGULAR).pack(padx=10, pady=15)
		tk.Label(self, bg=CODE_BG, text="Cảm ơn đã xem", font=FONT_REGULAR).pack(side='bottom', padx=10, pady=15)

		button = ttk.Button(self,
							text="Back to home",
							command=lambda: controlling.show(BeginPage))
		button.pack(side='bottom', padx=10, pady=15)

class classifyLeaf(tk.Frame):
	def __init__(self, parent, controlling):
		tk.Frame.__init__(self, master=parent)
		tk.Frame.configure(self, bg=CODE_BG)
		# self.columnconfigure(0, weight=1)
		# self.rowconfigure(0, weight=1)
		# Camera Area
		self.cam = ttk.LabelFrame(self, text="Display", width=480, height=360)
		self.cam.grid(row=0, column=0, padx=10, pady=10, sticky="ewns")
		self.cam.rowconfigure(0, weight=1)
		self.cam.columnconfigure(0, weight=1)
		# Button Area
		buttons_frame = tk.Frame(self)
		buttons_frame.configure(bg=CODE_BG, height=360, width=100)
		buttons_frame.grid(row=0, column=1, sticky="ne")
		self.checkVar = tk.IntVar()
		self.checkVar.set(0)
		checkCam = tk.Checkbutton(buttons_frame, text='Using Camera',
								   variable= self.checkVar,
								   onvalue= 1, offvalue=0,
								   bg = CODE_BG, command = self.camable())
		checkCam.grid(row= 0, column=0, padx = 10, pady=10)
		btn_Video = ttk.Button(buttons_frame, text='Take Picture',
							   command=None)
		btn_Video.grid(row=1, column=0, padx=10, pady=10)

		btn_Data = ttk.Button(buttons_frame, text='Classification',
							  command=None)
		btn_Data.grid(row=2, column=0, padx=10, pady=10)

		btn_Back = ttk.Button(buttons_frame, text="Back To Home",
							  command=lambda: controlling.show(BeginPage))
		btn_Back.grid(row=3, column=0, padx=10, pady=10)

		# Text Area
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
		# self.thread = threading.Thread(target=self.videoLoop, args=()).start()
		self.thread = threading.Thread(target=self.camable, args=()).start()
		self.panel = None
		# controlling.wm_protocol('Delete', self.on_close())

	def camable(self):
		try:
			while not self.stopEvent.is_set():
				if (self.checkVar.get() == 1):
					print("able Cam")
				else:
					print("unable Cam")
		except RuntimeError:
			print('Error')
				# self.thread = threading.Thread(target= self.videoLoop, args=()).start()
	def videoLoop(self):
		self.vs = VideoStream(usePiCamera=0).start()
		try:
			while not self.stopEvent.is_set():
				self.frame = self.vs.read()
				self.frame = cv.resize(self.frame, (480, 360))
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

	def on_close(self):
		self.stopEvent.set()
		self.vs.stop()
		self.quit()


app = LeafApp()
app.mainloop()