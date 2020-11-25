from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure    #to use matplotlib install matplotlib,to install: go to cmd and type :python -m pip install -U matplotlib then python -m pip install -U pip
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk, ImageOps 
import tkinter.font as tkFont
import sqlite3
import numpy as np
import serial as sr
import time

mode = "AOO"	#Initialization mode: no pacing
HEIGHT = 600    #dimension of the starting window
WIDTH = 1000    #dimension of the starting window
USER_ON = None        #Indicate which user is logged in
CANVAS_BACKGROUND_COLOR = "#80aaff"

#Variables used in egram
VENT_SIGNAL = np.array([]) #ventrical signal
ART_SIGNAL = np.array([])  #artiary signal

root =tk.Tk()
root.title('Heart Pacemaker')
root.geometry("1100x600")

#LRL = Lower Rate Limit
#URL = Upper Rate Limit
#AMP = Atrial/Ventricular Amplitude
#PW = Atrial/Ventricular Pulse Width
#RP = Atrial/Ventricular Refractory Period
AOO_params = { 
	"LRL": 60 ,
	"URL": 120,
	"AMP": 3.75,
	"PW": 0.4 ,
	"RP": 250
} 
VOO_params = { 
	"LRL": 60 ,
	"URL": 120,
	"AMP": 3.75,
	"PW": 0.4 ,
	"RP": 320
} 
AAI_params = { 
	"LRL": 60 ,
	"URL": 120,
	"AMP": 3.5,
	"PW": 0.4 ,
	"RP": 250
} 
VVI_params = { 
	"LRL": 60 ,
	"URL": 120,
	"AMP": 3.5,
	"PW": 0.4 ,
	"RP": 320
}

#Variables to hold the value of the current sliders to use for displaying the values.
lvar = StringVar()
uvar = StringVar()
avar = StringVar()
pvar = StringVar()
rvar = StringVar()
  


#Call the Serial Initilization Function, Main Program Starts from here
def send_data(data):
    global ser
    init_serial()
    ser.write(data)
    ser.close()

def read_data():
    global ser
    init_serial()
    bytes = ser.readline() #Read from Serial Port
    ser.close()

#Background image
class Background(Frame):
    def __init__(self, master, *pargs):
        Frame.__init__(self, master, *pargs)

        self.image = Image.open("image/Background.jpg")
        self.img_copy= self.image.copy()

        self.background_image = ImageTk.PhotoImage(self.image)

        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)

    def _resize_image(self,event):

        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image =  self.background_image)


e = Background(root)
e.pack(fill=BOTH, expand=YES)

#Images required
start_image = Image.open("image/Start.png")
start_image = ImageTk.PhotoImage(start_image)

reg_image = Image.open("image/Register.png")
reg_image = ImageTk.PhotoImage(reg_image)

back_image = Image.open("image/Backward.png")
back_image = ImageTk.PhotoImage(back_image)

del_image = Image.open("image/delete.png")
del_image = ImageTk.PhotoImage(del_image)

#Define font styles
fontStyle1 = tkFont.Font(family="Blackadder ITC", size=25)
fontStyle2 = tkFont.Font(family="Times New Roman", size=10)
fontStyle3 = tkFont.Font(family="Blackadder ITC", size=15)
fontStyle4 = tkFont.Font(family="Times New Roman", size=13)
fontStyle5 = tkFont.Font(family="Times New Roman", size=25, weight="bold")
fontStyle6 = tkFont.Font(family="Times New Roman", size=15, weight="bold")

#inital username/passwords
USERNAME = ["---"]*10
PASSWORD = []
OID = [None]*10


Data = sqlite3.connect('Users.db')
c = Data.cursor()#data cursor

#fetch all of the data in database
c.execute("SELECT *, oid FROM address")
records = c.fetchall()

num = len(records)

USERNAME.clear()
PASSWORD.clear()
OID.clear()
for x in records:
	USERNAME.append(x[0])
	PASSWORD.append(x[1])
	OID.append(str(x[2]))

for x in range(10-num):
	USERNAME.append("---")
	OID.append("")

Data.commit()

Data.close()
global canvas_front

#Startup Screen
def frame1():
	Start.place_forget()
	canvas_reg.place_forget()
	canvas_log.place_forget()
	canvas_front.place(x = 150, y = 50)
	Pacemaker_sign.place_forget()


	Data = sqlite3.connect('Users.db')

	c = Data.cursor()#data cursor

	#fetch all of the data in database
	c.execute("SELECT *, oid FROM address")
	records = c.fetchall()
	num = len(records)

	USERNAME.clear()
	PASSWORD.clear()
	OID.clear()
	for x in records:
		USERNAME.append(x[0])
		PASSWORD.append(x[1])
		OID.append(str(x[2]))

	for x in range(10-num):
		USERNAME.append("---")
		OID.append("")

	#refresh the user names for each button
	User1.configure(text = "User: " + USERNAME[0])
	User2.configure(text = "User: " + USERNAME[1])
	User3.configure(text = "User: " + USERNAME[2])
	User4.configure(text = "User: " + USERNAME[3])
	User5.configure(text = "User: " + USERNAME[4])
	User6.configure(text = "User: " + USERNAME[5])
	User7.configure(text = "User: " + USERNAME[6])
	User8.configure(text = "User: " + USERNAME[7])
	User9.configure(text = "User: " + USERNAME[8])
	User10.configure(text = "User: " + USERNAME[9])

	Data.commit()

	Data.close()


#Login screen
def log(user_number):
	global username_label2
	canvas_front.place_forget()
	canvas_log.place(x = 350, y = 50)
	
	global USER_ON
	USER_ON = user_number
	username_label2.configure(text = "Username:  " + USERNAME[user_number])


#Delete a record from database
def delete_user(user_num):
	Data = sqlite3.connect('Users.db')

	c = Data.cursor()

	if(OID[user_num] != ""):
		c.execute("DELETE from address WHERE oid ="+ OID[user_num])

	Data.commit()

	Data.close()
	frame1()

def Reg():
	canvas_front.place_forget()
	canvas_reg.place(x = 350, y = 50)

def reg_username_password():
	Data = sqlite3.connect('Users.db')

	c = Data.cursor()#data cursor

	#write into the data base
	if(username_entry.get()!= "" and password_entry.get()!= "" and len(PASSWORD)<10):
		c.execute("INSERT INTO address VALUES (:username, :password)",
				{
					'username': username_entry.get(),
					'password': password_entry.get()
				}
			)
	elif(len(PASSWORD)>=10):
		reg_wrong.config(text = "Users full!")
	elif(username_entry.get()== "" and password_entry.get()== ""):
		reg_wrong.config(text = "Invalid Entry!")

	Data.commit()

	Data.close()

	if(username_entry.get()!= "" and password_entry.get()!= "" and len(PASSWORD)<10):
		frame1()

	username_entry.delete(0,END)
	password_entry.delete(0,END)
	

def program_frame():
	global connected
	text = password_entry2.get()
	password_entry2.delete(0,END) 					#Clear the entry
	if(text == PASSWORD[USER_ON]):					#Check if the password entered is correct
		canvas_interface.place(x = 50, y = 25)
		Diff_Pacemaker.place(rely = 0.008, relx = 0.45)		#Display if a new pacemaker is connected
		Diff_Pacemaker.after(2500,lambda: Diff_Pacemaker.config(text = ""))
		canvas_log.place_forget()
	else:
		pass_wrong = tk.Label(canvas_log, text = "Wrong Password, please try again!", font = fontStyle2 ,bg = CANVAS_BACKGROUND_COLOR)
		pass_wrong.place(relx = 0.26,rely = 0.55)
		#print(USERNAME)
		#print(PASSWORD)
	try:
		ser = sr.Serial('COM6', baudrate = 115200, timeout = 1)
		if ser.isOpen():
			canvas_interface.delete(connected)
			connected = canvas_interface.create_oval(10,10,20,20,fill = "green")
			connected_label.configure(text = 'Connected')
	except sr.serialutil.SerialException:
		print('No Device Detected')

#Configure sliders for the different pacing modes. Labels are changed and values are reset to last saved.
def mode_switch(m):
	global mode
	scales = ["LRL_scale.set(%d)", "URL_scale.set(%d)", "AMP_scale.set(%f)", "PW_scale.set(%f)", "RP_scale.set(%d)"]
	i = 0
	
	if m == "AOO":
		mode = "AOO"	#Change global mode

		#Show which mode the program is in visually
		AOO_mode.configure(relief=SUNKEN)
		VOO_mode.configure(relief=RAISED)
		AAI_mode.configure(relief=RAISED)
		VVI_mode.configure(relief=RAISED)

		#Change labels and scale values
		AMP_scale.configure(label="Atrial Amplitude", from_=0.0, to=5.0, resolution=0.05)
		PW_scale.configure(label="Atrial Pulse Width")
		RP_scale.configure(label="Atrial Refractory Period")
		LRL_att.configure(text="Lower Rate Limit:")
		URL_att.configure(text="Upper Rate Limit:")
		AMP_att.configure(text="Atrial Amplitude:")
		PW_att.configure(text="Atrial Pulse Width:")
		RP_att.configure(text="Atrial Refractory Period:", font=fontStyle6)

		#Load last saved values to the scales
		for e in AOO_params:
			exec(scales[i] % AOO_params[e])
			i=i+1
		lvar.set(str(AOO_params["LRL"]))
		uvar.set(str(AOO_params["URL"]))
		avar.set(str(AOO_params["AMP"]))
		pvar.set(str(AOO_params["PW"]))
		rvar.set(str(AOO_params["RP"]))

	elif m == "VOO":
		mode = "VOO"
		AOO_mode.configure(relief=RAISED)
		VOO_mode.configure(relief=SUNKEN)
		AAI_mode.configure(relief=RAISED)
		VVI_mode.configure(relief=RAISED)
		AMP_scale.configure(label="Ventricular Amplitude", from_=0.0, to=5.0, resolution=0.05)
		PW_scale.configure(label="Ventricular Pulse Width")
		RP_scale.configure(label="Ventricular Refractory Period")
		LRL_att.configure(text="Lower Rate Limit:")
		URL_att.configure(text="Upper Rate Limit:")
		AMP_att.configure(text="Ventricular Amplitude:")
		PW_att.configure(text="Ventricular Pulse Width:")
		RP_att.configure(text="Ventricular Refractory Period:", font=tkFont.Font(family="Times New Roman", size=13, weight="bold"))

		for e in VOO_params:
			exec(scales[i] % VOO_params[e])
			i=i+1
		lvar.set(str(VOO_params["LRL"]))
		uvar.set(str(VOO_params["URL"]))
		avar.set(str(VOO_params["AMP"]))
		pvar.set(str(VOO_params["PW"]))
		rvar.set(str(VOO_params["RP"]))
			
	elif m == "AAI":
		mode = "AAI"
		AOO_mode.configure(relief=RAISED)
		VOO_mode.configure(relief=RAISED)
		AAI_mode.configure(relief=SUNKEN)
		VVI_mode.configure(relief=RAISED)
		AMP_scale.configure(label="Atrial Amplitude", from_=0.0, to=7.0, resolution = 0.1 if(AMP_scale.get() >= 0.5 and AMP_scale.get() <= 3.2) else 0.5)
		PW_scale.configure(label="Atrial Pulse Width")
		RP_scale.configure(label="Atrial Refractory Period")
		LRL_att.configure(text="Lower Rate Limit:")
		URL_att.configure(text="Upper Rate Limit:")
		AMP_att.configure(text="Atrial Amplitude:")
		PW_att.configure(text="Atrial Pulse Width:")
		RP_att.configure(text="Atrial Refractory Period:", font=fontStyle6)

		for e in AAI_params:
			exec(scales[i] % AAI_params[e])
			i=i+1
		lvar.set(str(AAI_params["LRL"]))
		uvar.set(str(AAI_params["URL"]))
		avar.set(str(AAI_params["AMP"]))
		pvar.set(str(AAI_params["PW"]))
		rvar.set(str(AAI_params["RP"]))
			
	elif m == "VVI":
		mode = "VVI"
		AOO_mode.configure(relief=RAISED)
		VOO_mode.configure(relief=RAISED)
		AAI_mode.configure(relief=RAISED)
		VVI_mode.configure(relief=SUNKEN)
		AMP_scale.configure(label="Ventricular Amplitude", from_=0.0, to=7.0, resolution = 0.1 if(AMP_scale.get() >= 0.5 and AMP_scale.get() <= 3.2) else 0.5)
		PW_scale.configure(label="Ventricular Pulse Width")
		RP_scale.configure(label="Ventricular Refractory Period")
		LRL_att.configure(text="Lower Rate Limit:")
		URL_att.configure(text="Upper Rate Limit:")
		AMP_att.configure(text="Ventricular Amplitude:")
		PW_att.configure(text="Ventricular Pulse Width:")
		RP_att.configure(text="Ventricular Refractory Period:", font=tkFont.Font(family="Times New Roman", size=13, weight="bold"))
		
		for e in VVI_params:
			exec(scales[i] % VVI_params[e])
			i=i+1
		lvar.set(str(VVI_params["LRL"]))
		uvar.set(str(VVI_params["URL"]))
		avar.set(str(VVI_params["AMP"]))
		pvar.set(str(VVI_params["PW"]))
		rvar.set(str(VVI_params["RP"]))
		
#Save current scale values to mode-specified parameters
def save():
	global AOO_params, VOO_params, AAI_params, VVI_params
	scales = ["LRL_scale.get()", "URL_scale.get()", "AMP_scale.get()", "PW_scale.get()", "RP_scale.get()"]
	i = 0
	if mode == "AOO":
		for e in AOO_params:
			AOO_params[e] = eval(scales[i])
			i=i+1
		lvar.set(str(AOO_params["LRL"]))
		uvar.set(str(AOO_params["URL"]))
		avar.set(str(AOO_params["AMP"]))
		pvar.set(str(AOO_params["PW"]))
		rvar.set(str(AOO_params["RP"]))
	elif mode == "VOO":
		for e in VOO_params:
			VOO_params[e] = eval(scales[i])
			i=i+1
		lvar.set(str(VOO_params["LRL"]))
		uvar.set(str(VOO_params["URL"]))
		avar.set(str(VOO_params["AMP"]))
		pvar.set(str(VOO_params["PW"]))
		rvar.set(str(VOO_params["RP"]))
	elif mode == "AAI":
		for e in AAI_params:
			AAI_params[e] = eval(scales[i])
			i=i+1
		lvar.set(str(AAI_params["LRL"]))
		uvar.set(str(AAI_params["URL"]))
		avar.set(str(AAI_params["AMP"]))
		pvar.set(str(AAI_params["PW"]))
		rvar.set(str(AAI_params["RP"]))
	elif mode == "VVI":
		for e in VVI_params:
			VVI_params[e] = eval(scales[i])
			i=i+1
		lvar.set(str(VVI_params["LRL"]))
		uvar.set(str(VVI_params["URL"]))
		avar.set(str(VVI_params["AMP"]))
		pvar.set(str(VVI_params["PW"]))
		rvar.set(str(VVI_params["RP"]))

#change_XXX_res functions account for the different resolutions in different ranges for each scale
def change_LRL_res(r):
	LRL_scale.configure(resolution = 1 if(float(LRL_scale.get()) >= 49.5 and float(LRL_scale.get()) <= 90) else 5)
	if LRL_scale.get() > URL_scale.get():
		URL_scale.set(LRL_scale.get())

def change_AMP_res(r):
	if mode == "AAI" or mode == "VVI":
		AMP_scale.configure(from_=0.0, to=7.0, resolution = 0.1 if(AMP_scale.get() >= 0.5 and AMP_scale.get() <= 3.2) else 0.5)
	else:
		if float(r) <= 1:
			AMP_scale.set(0)
		elif float(r) >= 1 and float(r) <= 2:
			AMP_scale.set(1.25)
		elif float(r) > 2 and float(r) <= 3:
			AMP_scale.set(2.5)
		elif float(r) >= 3 and float(r) <= 4:
			AMP_scale.set(3.75)
		elif float(r) >= 4:
			AMP_scale.set(5)
	

def change_PW_res(r):
	PW_scale.configure(resolution = 0.05 if(PW_scale.get() <= 0.1) else 0.1)
	if PW_scale.get() == 0:
		PW_scale.set(0.05)

def change_URL_lim(l):
	if LRL_scale.get() > URL_scale.get():
		LRL_scale.set(URL_scale.get())

def egram():
	print("hi")
	new_window = tk.Toplevel(root)
	new_window.title("Egram Graph")
	new_window.geometry("700x500")
	text = tk.Label(new_window,text = "New window")
	text.place(relx=0.5,rely = 0.5)



#USED TO SHOW ALL THE PARAMETER !! BEST TO KEEP THIS FUNCTION AT THE END OF ALL FUNCTIONS
def show():
	print("Show all the users and their passwords")
	print(USERNAME)
	print(PASSWORD)
	print("AOO parameters: ")
	print("\tLRL: " + str(AOO_params["LRL"]) + "\t\tURL: " + str(AOO_params["URL"]) + "\tAMP: " + str(AOO_params["AMP"]) + "\tPW: " + str(AOO_params["PW"]) + "\tRP: " + str(AOO_params["RP"]))
	print("VOO parameters: ")
	print("\tLRL: " + str(VOO_params["LRL"]) + "\t\tURL: " + str(VOO_params["URL"]) + "\tAMP: " + str(VOO_params["AMP"]) + "\tPW: " + str(VOO_params["PW"]) + "\tRP: " + str(VOO_params["RP"]))
	print("AAI parameters: ")
	print("\tLRL: " + str(AAI_params["LRL"]) + "\t\tURL: " + str(AAI_params["URL"]) + "\tAMP: " + str(AAI_params["AMP"]) + "\tPW: " + str(AAI_params["PW"]) + "\tRP: " + str(AAI_params["RP"]))
	print("VVI parameters: ")
	print("\tLRL: " + str(VVI_params["LRL"]) + "\t\tURL: " + str(VVI_params["URL"]) + "\tAMP: " + str(VVI_params["AMP"]) + "\tPW: " + str(VVI_params["PW"]) + "\tRP: " + str(VVI_params["RP"]))

# Databases
# Create a username database
'''
Data = sqlite3.connect('Users.db')

c = Data.cursor()#data cursor

#create database for the first time commented after
c.execute("""CREATE TABLE address(
		username text,
		password text)
	""")

Data.commit()

Data.close()
'''

#Starting Page:
Pacemaker_sign=tk.Label(root, text = "Pacemaker Interface", font = fontStyle1, bg = "#3333ff", fg = "#ffff80")
Pacemaker_sign.place(relx = 0.1, rely = 0.15)

Start = tk.Button(root, image = start_image, command = frame1)
Start.place(relx = 0.76, rely=0.5)

#Button used to show all parameters
Show = tk.Button(root, text = "Show",font = tkFont.Font(size=5), command = show)
Show.place(relx = 0.5, rely = 0.01)


#User list front canvas
canvas_front = tk.Canvas(root, height = HEIGHT-100, width = WIDTH-200, bg = CANVAS_BACKGROUND_COLOR)

User1 = tk.Button(canvas_front, text = "User: " + USERNAME[0], width = 30, height = 2, font = fontStyle2, command = lambda: log(0))
User2 = tk.Button(canvas_front, text = "User: " + USERNAME[1], width = 30, height = 2, font = fontStyle2, command = lambda: log(1))
User3 = tk.Button(canvas_front, text = "User: " + USERNAME[2], width = 30, height = 2, font = fontStyle2, command = lambda: log(2))
User4 = tk.Button(canvas_front, text = "User: " + USERNAME[3], width = 30, height = 2, font = fontStyle2, command = lambda: log(3))
User5 = tk.Button(canvas_front, text = "User: " + USERNAME[4], width = 30, height = 2, font = fontStyle2, command = lambda: log(4))
User6 = tk.Button(canvas_front, text = "User: " + USERNAME[5], width = 30, height = 2, font = fontStyle2, command = lambda: log(5))
User7 = tk.Button(canvas_front, text = "User: " + USERNAME[6], width = 30, height = 2, font = fontStyle2, command = lambda: log(6))
User8 = tk.Button(canvas_front, text = "User: " + USERNAME[7], width = 30, height = 2, font = fontStyle2, command = lambda: log(7))
User9 = tk.Button(canvas_front, text = "User: " + USERNAME[8], width = 30, height = 2, font = fontStyle2, command = lambda: log(8))
User10 = tk.Button(canvas_front, text = "User: " + USERNAME[9], width = 30, height = 2, font = fontStyle2, command = lambda: log(9))

u1_del = tk.Button(canvas_front, image = del_image, command = lambda: delete_user(0))
u2_de2 = tk.Button(canvas_front, image = del_image, command = lambda: delete_user(1))
u3_de3 = tk.Button(canvas_front, image = del_image, command = lambda: delete_user(2))
u4_de4 = tk.Button(canvas_front, image = del_image, command = lambda: delete_user(3))
u5_de5 = tk.Button(canvas_front, image = del_image, command = lambda: delete_user(4))
u6_de6 = tk.Button(canvas_front, image = del_image, command = lambda: delete_user(5))
u7_de7 = tk.Button(canvas_front, image = del_image, command = lambda: delete_user(6))
u8_de8 = tk.Button(canvas_front, image = del_image, command = lambda: delete_user(7))
u9_de9 = tk.Button(canvas_front, image = del_image, command = lambda: delete_user(8))
u10_del0 = tk.Button(canvas_front, image = del_image, command = lambda: delete_user(9))

Register = tk.Button(canvas_front, image = reg_image, command = Reg)

User1.place(relx = 0.1, rely = 0.15)
User2.place(relx = 0.6, rely = 0.15)
User3.place(relx = 0.1, rely = 0.3)
User4.place(relx = 0.6, rely = 0.3)
User5.place(relx = 0.1, rely = 0.45)
User6.place(relx = 0.6, rely = 0.45)
User7.place(relx = 0.1, rely = 0.6)
User8.place(relx = 0.6, rely = 0.6)
User9.place(relx = 0.1, rely = 0.75)
User10.place(relx = 0.6, rely = 0.75)

u1_del.place(relx = 0.38, rely = 0.16)
u2_de2.place(relx = 0.88, rely = 0.16)
u3_de3.place(relx = 0.38, rely = 0.31)
u4_de4.place(relx = 0.88, rely = 0.31)
u5_de5.place(relx = 0.38, rely = 0.46)
u6_de6.place(relx = 0.88, rely = 0.46)
u7_de7.place(relx = 0.38, rely = 0.61)
u8_de8.place(relx = 0.88, rely = 0.61)
u9_de9.place(relx = 0.38, rely = 0.76)
u10_del0.place(relx = 0.88, rely = 0.76)

Register.place(relx =0.82,rely = 0.87)


#Register canvas
canvas_reg = tk.Canvas(root, height = 500, width = 400, bg = CANVAS_BACKGROUND_COLOR)

submit_button = tk.Button(canvas_reg, text = "Submit", command = reg_username_password)
back_button = tk.Button(canvas_reg, image= back_image, command = frame1)
username_label=tk.Label(canvas_reg, text = "Username: ", font = fontStyle3, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000")
username_entry=tk.Entry(canvas_reg,font= fontStyle2)
password_label=tk.Label(canvas_reg, text = "Password: ", font = fontStyle3, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000")
password_entry=tk.Entry(canvas_reg,font= fontStyle2)
reg_wrong =tk.Label(canvas_reg,text ="", font = fontStyle2 ,bg = CANVAS_BACKGROUND_COLOR)


submit_button.place(relx = 0.8, rely = 0.9)
back_button.place(relx = 0.2, rely = 0.88)
username_label.place(relx = 0.25, rely = 0.38)
username_entry.place(relx = 0.45,rely = 0.4, relwidth = 0.3)
password_label.place(relx = 0.25, rely = 0.48)
password_entry.place(relx = 0.45,rely = 0.5, relwidth = 0.3)
reg_wrong.place(relx=0.4,rely=0.55)


#Log in Canvas
canvas_log = tk.Canvas(root, height = 500, width = 400, bg = CANVAS_BACKGROUND_COLOR)

submit_button2 = tk.Button(canvas_log, text = "Submit", command = program_frame)
back_button2 = tk.Button(canvas_log, image= back_image, command = frame1)
password_label2=tk.Label(canvas_log, text = "Password: ", font = fontStyle3, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000")
password_entry2=tk.Entry(canvas_log,font= fontStyle2)
username_label2 = tk.Label(canvas_log, text = "Username:  ", font = fontStyle3, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000")

submit_button2.place(relx = 0.8, rely = 0.9)
back_button2.place(relx = 0.2, rely = 0.88)
password_label2.place(relx = 0.25, rely = 0.48)
password_entry2.place(relx = 0.45,rely = 0.5, relwidth = 0.3)
username_label2.place(relx = 0.25, rely = 0.38)



#USER INTERFACE CANVAS
canvas_interface = tk.Canvas(root, height = HEIGHT-50, width = WIDTH, bg = CANVAS_BACKGROUND_COLOR)

#Show pacemaker connected status. Check if new device is connected
connected = canvas_interface.create_oval(10,10,20,20,fill = "red")
connected_label = tk.Label(canvas_interface, text = "Not Connected", font = tkFont.Font(size=10), bg = CANVAS_BACKGROUND_COLOR, fg = "#990000")
Diff_Pacemaker = tk.Label(canvas_interface, text = "A New Pacemaker detected", font = tkFont.Font(size=10), bg = CANVAS_BACKGROUND_COLOR, fg = "#990000")

connected_label.place(rely = 0.008, relx = 0.025)

#Egram window button
EGRAM_WINDOW = tk.Button(canvas_interface, text = "EGRAM", font = tkFont.Font(size=6), bg = CANVAS_BACKGROUND_COLOR, fg = "#990000",command = egram)

EGRAM_WINDOW.place(rely = 0.008, relx = 0.95)

#Mode switching buttons
AOO_mode = tk.Button(canvas_interface, text = "AOO", width=12, pady=6, font = fontStyle1, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000", relief=SUNKEN, command = lambda: mode_switch("AOO"))
VOO_mode = tk.Button(canvas_interface, text = "VOO", width=12, pady=6, font = fontStyle1, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000", command = lambda: mode_switch("VOO"))
AAI_mode = tk.Button(canvas_interface, text = "AAI", width=12, pady=6, font = fontStyle1, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000", command = lambda: mode_switch("AAI"))
VVI_mode = tk.Button(canvas_interface, text = "VVI", width=12, pady=6, font = fontStyle1, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000", command = lambda: mode_switch("VVI"))

AOO_mode.place(rely=0.0475, relx=0.002)
VOO_mode.place(rely=0.0475, relx = 0.251)
AAI_mode.place(rely=0.0475, relx = 0.5)
VVI_mode.place(rely=0.0475, relx = 0.749)

#Sliders to change the parameter values
LRL_scale =Scale(canvas_interface, orient=HORIZONTAL, length=600, width=35, sliderlength="60", label="Lower Rate Limit", font = fontStyle4, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=30, to=175, resolution=1, command=change_LRL_res)
URL_scale =Scale(canvas_interface, orient=HORIZONTAL, length=600, width=35, sliderlength="60", label="Upper Rate Limit", font = fontStyle4, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=30, to=175, resolution=5, command=change_URL_lim)
AMP_scale =Scale(canvas_interface, orient=HORIZONTAL, length=600, width=35, sliderlength="60", label="Atrial Amplitude", font = fontStyle4, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=0.0, to=5.0, resolution=0.05, command=change_AMP_res)
PW_scale = Scale(canvas_interface, orient=HORIZONTAL, length=600, width=35, sliderlength="60", label="Atrial Pulse Width", font = fontStyle4, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=0, to=1.9, resolution=0.05,  command=change_PW_res)
RP_scale = Scale(canvas_interface, orient=HORIZONTAL, length=600, width=35, sliderlength="60", label="Atrial Refractory Period", font = fontStyle4, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=150, to=500, resolution = 10)

LRL_scale.place(relx = 0.0325, rely = 0.2)
URL_scale.place(relx = 0.0325, rely = 0.35)
AMP_scale.place(relx = 0.0325, rely = 0.5)
PW_scale.place( relx = 0.0325, rely = 0.65)
RP_scale.place( relx = 0.0325, rely = 0.8)

#AOO nominal values
LRL_scale.set(60)
URL_scale.set(120)
AMP_scale.set(3.75)
PW_scale.set(0.4)
RP_scale.set(250)

att = LabelFrame(canvas_interface, text="Attributes", bg="white", fg="#990000", font = fontStyle5, height=419, width=335, labelanchor=N, relief=RAISED)

#Display parameter values
LRL_att = Label(att, text="Lower Rate Limit:", font=fontStyle6, bg="white")
URL_att = Label(att, text="Upper Rate Limit:", font=fontStyle6, bg="white")
AMP_att = Label(att, text="Atrial Amplitude:", font=fontStyle6, bg="white")
PW_att =  Label(att, text="Atrial Pulse Width:", font=fontStyle6, bg="white")
RP_att =  Label(att, text="Atrial Refractory Period:", font=fontStyle6, bg="white")
LRL_val = Label(att, textvariable=lvar, font=fontStyle6, bg="white", fg="#990000", width=4, relief=RIDGE)
URL_val = Label(att, textvariable=uvar, font=fontStyle6, bg="white", fg="#990000", width=4, relief=RIDGE)
AMP_val = Label(att, textvariable=avar, font=fontStyle6, bg="white", fg="#990000", width=4, relief=RIDGE)
PW_val =  Label(att, textvariable=pvar, font=fontStyle6, bg="white", fg="#990000", width=4, relief=RIDGE)
RP_val =  Label(att, textvariable=rvar, font=fontStyle6, bg="white", fg="#990000", width=4, relief=RIDGE)

lvar.set(str(AOO_params["LRL"]))
uvar.set(str(AOO_params["URL"]))
avar.set(str(AOO_params["AMP"]))
pvar.set(str(AOO_params["PW"]))
rvar.set(str(AOO_params["RP"]))

att.place(relx=0.635, rely=0.2)
LRL_att.place(relx=0.035, rely=0.1)
LRL_val.place(relx=0.75, rely=0.1)
URL_att.place(relx=0.035, rely=0.25)
URL_val.place(relx=0.75, rely=0.25)
AMP_att.place(relx=0.035, rely=0.4)
AMP_val.place(relx=0.75, rely=0.4)
PW_att.place(relx=0.035, rely=0.55)
PW_val.place(relx=0.75, rely=0.55)
RP_att.place(relx=0.035, rely=0.7)
RP_val.place(relx=0.75, rely=0.7)

set_butt = Button(att, text = "Accept Values", padx=106.25, font = fontStyle3, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000", command=save)

set_butt.place(rely=0.8775)



root.mainloop() 