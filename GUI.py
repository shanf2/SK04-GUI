from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure    #to use matplotlib install matplotlib,to install: go to cmd and type :python -m pip install -U matplotlib then python -m pip install -U pip
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk, ImageOps 
import tkinter.font as tkFont
import numpy as np
import serial as sr
import time
import parameters as P
import db_utilities as db
from struct import *

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

params = P.Parameters()

#Variables to hold the value of the current sliders to use for displaying the values.
lvar = StringVar()
uvar = StringVar()
avar = StringVar()
pvar = StringVar()
rvar = StringVar()

ser =sr
#Initialize the serial communication
def init_serial():
	global ser
	global connected
	global header
	try:
		ser = sr.Serial('COM6', baudrate = 115200, bytesize=sr.EIGHTBITS , timeout = 1)
		if ser.isOpen():
			header.delete(connected)
			connected = header.create_oval(80,5,90,15,fill = "green")
			connected_label.configure(text = 'Connected')
			print('connected')
			ser.close()
	except sr.serialutil.SerialException:
		header.delete(connected)
		connected = header.create_oval(100,5,110,15,fill = "red")
		connected_label.configure(text = 'Not Connected')
		print('No Device Detected')

#Call the Serial Initilization Function, Main Program Starts from here
def send_data():
    global ser
    if(ser.isOpen()==False):
    	init_serial()
    ser.open()
    '''
	serial_status = 0x16
	serial_write = 0x55
	serial_mode = params.mode
	serial_LRL = params.lrl
	serial_URL = params.url
	serial_A_Amplitude = params.a_amp
	serial_V_Amplitude = params.v_amp
	serial_Pulsewidth = params.pw
	serial_A_Sensitivity = params.a_sensi
	serial_V_Sensitivity = params.v_sensi
	serial_Refractory = params.rp
	serial_AV_Delay = params.av_delay
	serial_Activity_Threshold = params.act_thresh
	serial_Reaction_time = params.react_t
	serial_Resopnse_factor = params.res_fact
	serial_Recovery_time = params.rec_t

	serial_data = pack('>BBBBBHHHHHHHHBHH',serial_status,serial_write,serial_mode,serial_LRL,serial_URL,serial_A_Amplitude,
						serial_V_Amplitude,serial_Pulsewidth,serial_A_Sensitivity,serial_V_Sensitivity,serial_Refractory,serial_Hysterisis,
						serial_MSR,serial_Activity_Threshold,serial_Reaction_time,serial_Resopnse_factor,serial_Recovery_time)
	'''
    ser.write(serial_Data)
    ser.close()


def echo_data():
    global ser


    ser.open()
    #ser.reset_input_buffer()
    serial_status = 22
    serial_write = 34

    serial_data = pack('>BB',22,34)
    print(ser.name)

    #ser.write(serial_data)
    print(serial_data)

    ser.write(serial_data)
    s = ser.read(26) # read up to ten bytes (timeout)
    #line = sr.readline()              

    data_recevied = ser.read(26) #Read from Serial Port

    #a = unpack('>BBBBBHHHHHHHHBHH',s)

    '''

    serial_status = 0x16
	serial_write = 0x22
	serial_mode = params.mode
	serial_LRL = params.lrl
	serial_URL = params.url
	serial_A_Amplitude = params.a_amp
	serial_V_Amplitude = params.v_amp
	serial_Pulsewidth = params.pw
	serial_A_Sensitivity = params.a_sensi
	serial_V_Sensitivity = params.v_sensi
	serial_Refractory = params.rp
	serial_AV_Delay = params.av_delay
	serial_Activity_Threshold = params.act_thresh
	serial_Reaction_time = params.react_t
	serial_Resopnse_factor = params.res_fact
	serial_Recovery_time = params.rec_t 
    '''
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
fontStyle3 = tkFont.Font(family="Blackadder ITC", size=15, weight="bold")
fontStyle4 = tkFont.Font(family="Times New Roman", size=13)
fontStyle5 = tkFont.Font(family="Times New Roman", size=25, weight="bold")
fontStyle6 = tkFont.Font(family="Times New Roman", size=15, weight="bold")
fontStyle7 = tkFont.Font(family="Times New Roman", size=10)
fontStyle8 = tkFont.Font(family="Blackadder ITC", size=13, weight="bold")
fontStyle9 = tkFont.Font(family="Times New Roman", size=13, weight="bold")

#inital username/passwords
USERNAME = ["---"]*10
PASSWORD = []
OID = [None]*10


Data = db.conn('Users.db')
records = db.fetch_users(Data)

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


global canvas_front

#Startup Screen
def frame1():
	Start.place_forget()
	canvas_reg.place_forget()
	canvas_log.place_forget()
	canvas_front.place(x = 150, y = 50)
	Pacemaker_sign.place_forget()


	Data = db.conn('Users.db')
	records = db.fetch_users(Data)

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

	reg_wrong.config(text="")
	pass_wrong.config(text="")


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
	Data = db.conn('Users.db')
	db.delete(Data, OID[user_num])
	frame1()

def Reg():
	canvas_front.place_forget()
	canvas_reg.place(x = 350, y = 50)

def reg_username_password():
	Data = db.conn('Users.db')

	#write into the data base
	if(username_entry.get()!= "" and password_entry.get()!= "" and len(PASSWORD)<10):
		db.register(Data, username_entry.get(), password_entry.get())
		frame1()
	elif(len(PASSWORD)>=10):
		reg_wrong.config(text = "Users full!")
	elif(username_entry.get()== "" and password_entry.get()== ""):
		reg_wrong.config(text = "Invalid Entry!")


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
		init_serial()
	else:
		pass_wrong.config(text="Wrong password, please try again!")
		#print(USERNAME)
		#print(PASSWORD)

#Configure sliders for the different pacing modes. Labels are changed and values are reset to last saved.
def mode_switch(m):
	global mode
	scales = ["lrl_scale.set(%d)", "url_scale.set(%d)", "a_amp_scale.set(%f)", "pw_scale.set(%f)", "rp_scale.set(%d)"]
	i = 0
	
	if m == "AOO":
		mode = "AOO"	#Change global mode

		#Show which mode the program is in visually
		AOO_mode.configure(relief=SUNKEN)
		VOO_mode.configure(relief=RAISED)
		AAI_mode.configure(relief=RAISED)
		VVI_mode.configure(relief=RAISED)

		#Change labels and scale values
		a_amp_scale.configure(label="Atrial Amplitude", from_=0.0, to=5.0, resolution=0.05)
		pw_scale.configure(label="Atrial Pulse Width")
		rp_scale.configure(label="Atrial Refractory Period")
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
		a_amp_scale.configure(label="Ventricular Amplitude", from_=0.0, to=5.0, resolution=0.05)
		pw_scale.configure(label="Ventricular Pulse Width")
		rp_scale.configure(label="Ventricular Refractory Period")
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
		a_amp_scale.configure(label="Atrial Amplitude", from_=0.0, to=7.0, resolution = 0.1 if(a_amp_scale.get() >= 0.5 and a_amp_scale.get() <= 3.2) else 0.5)
		pw_scale.configure(label="Atrial Pulse Width")
		rp_scale.configure(label="Atrial Refractory Period")
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
		settings = '''
AOO_mode.configure(relief=RAISED)
VOO_mode.configure(relief=RAISED)
AAI_mode.configure(relief=RAISED)
VVI_mode.configure(relief=SUNKEN)
a_amp_scale.configure(label="Ventricular Amplitude", from_=0.0, to=7.0, resolution = 0.1 if(a_amp_scale.get() >= 0.5 and a_amp_scale.get() <= 3.2) else 0.5)
pw_scale.configure(label="Ventricular Pulse Width")
rp_scale.configure(label="Ventricular Refractory Period")
LRL_att.configure(text="Lower Rate Limit:")
URL_att.configure(text="Upper Rate Limit:")
AMP_att.configure(text="Ventricular Amplitude:")
PW_att.configure(text="Ventricular Pulse Width:")
RP_att.configure(text="Ventricular Refractory Period:", font=tkFont.Font(family="Times New Roman", size=13, weight="bold"))
		'''
		exec(settings)
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
	scales = ["lrl_scale.get()", "url_scale.get()", "a_amp_scale.get()", "pw_scale.get()", "rp_scale.get()"]
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

def change_LRL_res(r):
	lrl_scale.configure(resolution = 1 if(lrl_scale.get() > 49 and lrl_scale.get() < 91) else 5)
	if lrl_scale.get() > url_scale.get():
		url_scale.set(lrl_scale.get())

def change_URL_lim(l):
	if lrl_scale.get() > url_scale.get():
		lrl_scale.set(url_scale.get())

'''
#change_XXX_res functions account for the different resolutions in different ranges for each scale

def change_AMP_res(r):
	if mode == "AAI" or mode == "VVI":
		a_amp_scale.configure(from_=0.0, to=7.0, resolution = 0.1 if(a_amp_scale.get() >= 0.5 and a_amp_scale.get() <= 3.2) else 0.5)
	else:
		if float(r) <= 1:
			a_amp_scale.set(0)
		elif float(r) >= 1 and float(r) <= 2:
			a_amp_scale.set(1.25)
		elif float(r) > 2 and float(r) <= 3:
			a_amp_scale.set(2.5)
		elif float(r) >= 3 and float(r) <= 4:
			a_amp_scale.set(3.75)
		elif float(r) >= 4:
			a_amp_scale.set(5)
	

def change_PW_res(r):
	pw_scale.configure(resolution = 0.05 if(pw_scale.get() <= 0.1) else 0.1)
	if pw_scale.get() == 0:
		pw_scale.set(0.05)

'''
def egram():
	print("hi")
	new_window = tk.Toplevel(root)
	new_window.title("Egram Graph")
	new_window.geometry("700x500")
	text = tk.Label(new_window,text = "New window")
	text.place(relx=0.5,rely = 0.5)
	read_data()



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
pass_wrong = tk.Label(canvas_log, text = "Wrong Password, please try again!", font = fontStyle2 ,bg = CANVAS_BACKGROUND_COLOR)

submit_button2.place(relx = 0.8, rely = 0.9)
back_button2.place(relx = 0.2, rely = 0.88)
password_label2.place(relx = 0.25, rely = 0.48)
password_entry2.place(relx = 0.45,rely = 0.5, relwidth = 0.3)
username_label2.place(relx = 0.25, rely = 0.38)
pass_wrong.place(relx = 0.26,rely = 0.55)



#USER INTERFACE CANVAS
canvas_interface = tk.Frame(root, height = HEIGHT-50, width = WIDTH, bg = CANVAS_BACKGROUND_COLOR)


header = tk.Canvas(canvas_interface, height=20, width=WIDTH-50, bg=CANVAS_BACKGROUND_COLOR, bd=0, highlightthickness=0)
footer = tk.Canvas(canvas_interface, height=20, width=WIDTH-50, bg=CANVAS_BACKGROUND_COLOR, bd=0, highlightthickness=0)
left = tk.Frame(canvas_interface, bg=CANVAS_BACKGROUND_COLOR, width=25, height=HEIGHT-50)
right = tk.Frame(canvas_interface, bg=CANVAS_BACKGROUND_COLOR, width=25, height=HEIGHT-50)
foot_label = tk.Label(header, text = " ", font = tkFont.Font(size=10), bg = CANVAS_BACKGROUND_COLOR, fg = "#990000")
header.grid(row=0, column=1, columnspan=6, sticky="NSEW")
footer.grid(row=10, column=1, columnspan=6, sticky="NSEW")
left.grid(row=0, column=0, rowspan=11)
right.grid(row=0, column=7, rowspan=11)
foot_label.grid(row=0, column=1, columnspan=6)

#Show pacemaker connected status. Check if new device is connected
connected_label = tk.Label(header, text = "Not Connected", font = tkFont.Font(size=10), bg = CANVAS_BACKGROUND_COLOR, fg = "#990000")
Diff_Pacemaker = tk.Label(header, text = "A New Pacemaker detected", font = tkFont.Font(size=10), bg = CANVAS_BACKGROUND_COLOR, fg = "#990000")
connected = header.create_oval(100,5,110,15,fill = "red")

connected_label.grid(row=0, column=1, columnspan=6)

#Egram window button
EGRAM_WINDOW = tk.Button(canvas_interface, text = "EGRAM", font = fontStyle6, bg = "#002DA4", fg = "#FFFFFF",command = egram)

EGRAM_WINDOW.grid(row=2, column=6, sticky="NSEW")

#Mode switching buttons
AOO_mode = tk.Button(canvas_interface, text = "AOO", font = fontStyle8, width=12, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000", command = lambda: params.mode_switch("AOO"), relief=SUNKEN)
VOO_mode = tk.Button(canvas_interface, text = "VOO", font = fontStyle8, width=12, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000", command = lambda: params.mode_switch("VOO"))
AAI_mode = tk.Button(canvas_interface, text = "AAI", font = fontStyle8, width=12, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000", command = lambda: params.mode_switch("AAI"))
VVI_mode = tk.Button(canvas_interface, text = "VVI", font = fontStyle8, width=12, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000", command = lambda: params.mode_switch("VVI"))
DOO_mode = tk.Button(canvas_interface, text = "DOO", font = fontStyle8, width=12, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000", command = lambda: params.mode_switch("DOO"))
AOOR_mode = tk.Button(canvas_interface, text = "AOOR", font = fontStyle8, width=12, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000", command = lambda: params.mode_switch("AOOR"))
VOOR_mode = tk.Button(canvas_interface, text = "VOOR", font = fontStyle8, width=12, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000", command = lambda: params.mode_switch("VOOR"))
AAIR_mode = tk.Button(canvas_interface, text = "AAIR", font = fontStyle8, width=12, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000", command = lambda: params.mode_switch("AAIR"))
VVIR_mode = tk.Button(canvas_interface, text = "VVIR", font = fontStyle8, width=12, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000", command = lambda: params.mode_switch("VVIR"))
DOOR_mode = tk.Button(canvas_interface, text = "DOOR", font = fontStyle8, width=12, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000", command = lambda: params.mode_switch("DOOR"))
DDDR_mode = tk.Button(canvas_interface, text = "DDDR", font = fontStyle8, width=12, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000", command = lambda: params.mode_switch("DDDR"))

AOO_mode.grid(row=1, column=1, sticky="NSEW")
VOO_mode.grid(row=1, column=2, sticky="NSEW")
AAI_mode.grid(row=1, column=3, sticky="NSEW")
VVI_mode.grid(row=1, column=4, sticky="NSEW")
DOO_mode.grid(row=1, column=5, sticky="NSEW")
AOOR_mode.grid(row=2, column=1, sticky="NSEW")
VOOR_mode.grid(row=2, column=2, sticky="NSEW")
AAIR_mode.grid(row=2, column=3, sticky="NSEW")
VVIR_mode.grid(row=2, column=4, sticky="NSEW")
DOOR_mode.grid(row=2, column=5, sticky="NSEW")
DDDR_mode.grid(row=1, column=6, sticky="NSEW")

for i in range(8):
	if(i==0 or i==7): canvas_interface.grid_columnconfigure(i, weight=1)
	else: canvas_interface.grid_columnconfigure(i, weight=3)
for i in range(11):
	if(i==0 or i==10): canvas_interface.grid_rowconfigure(i, weight=1)
	else: canvas_interface.grid_rowconfigure(i, weight=2)

#Sliders to change the parameter values
lrl_scale =		   Scale(canvas_interface, orient=HORIZONTAL, width=18, sliderlength="30", label="Lower Rate Limit", font = fontStyle7, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=30, to=175, resolution=1)
url_scale =		   Scale(canvas_interface, orient=HORIZONTAL, width=18, sliderlength="30", label="Upper Rate Limit", font = fontStyle7, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=50, to=175, resolution=5)
a_amp_scale =	   Scale(canvas_interface, orient=HORIZONTAL, width=18, sliderlength="30", label="Atrial Amplitude", font = fontStyle7, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=0, to=5000, resolution=100)
v_amp_scale =	   Scale(canvas_interface, orient=HORIZONTAL, width=18, sliderlength="30", label="Ventricular Amplitude", font = fontStyle7, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=0, to=5000, resolution=100)
pw_scale =		   Scale(canvas_interface, orient=HORIZONTAL, width=18, sliderlength="30", label="Pulse Width", font = fontStyle7, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=1, to=30, resolution=1)
a_sensi_scale =	   Scale(canvas_interface, orient=HORIZONTAL, width=18, sliderlength="30", label="Atrial Sensitivity", font = fontStyle7, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=0, to=5000, resolution=100)
v_sensi_scale =	   Scale(canvas_interface, orient=HORIZONTAL, width=18, sliderlength="30", label="Ventricular Sensitivity", font = fontStyle7, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=0, to=5000, resolution=100)
rp_scale =		   Scale(canvas_interface, orient=HORIZONTAL, width=18, sliderlength="30", label="A/V Refractory Period", font = fontStyle7, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=150, to=500, resolution=10)
av_delay_scale =   Scale(canvas_interface, orient=HORIZONTAL, width=18, sliderlength="30", label="A/V Delay", font = fontStyle7, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=70, to=300, resolution=10)
msr_scale =		   Scale(canvas_interface, orient=HORIZONTAL, width=18, sliderlength="30", label="Maximum Sensor Rate", font = fontStyle7, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=50, to=175, resolution=5)
act_thresh_scale = Scale(canvas_interface, orient=HORIZONTAL, width=18, sliderlength="30", label="Activity Threshold", font = fontStyle7, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=1, to=7, resolution=1)
react_t_scale =	   Scale(canvas_interface, orient=HORIZONTAL, width=18, sliderlength="30", label="Reaction Time", font = fontStyle7, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=10, to=50, resolution=10)
res_fact_scale =   Scale(canvas_interface, orient=HORIZONTAL, width=18, sliderlength="30", label="Response Factor", font = fontStyle7, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=1, to=16, resolution=1)
rec_t_scale =	   Scale(canvas_interface, orient=HORIZONTAL, width=18, sliderlength="30", label="Recovery Time", font = fontStyle7, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=120, to=960, resolution=60)

lrl_scale.grid(row=3, column=1, columnspan=2, sticky="NSEW")
url_scale.grid(row=4, column=1, columnspan=2, sticky="NSEW")
a_amp_scale.grid(row=5, column=1, columnspan=2, sticky="NSEW")
v_amp_scale.grid(row=6, column=1, columnspan=2, sticky="NSEW")
pw_scale.grid(row=7, column=1, columnspan=2, sticky="NSEW")
a_sensi_scale.grid(row=8, column=1, columnspan=2, sticky="NSEW")
v_sensi_scale.grid(row=9, column=1, columnspan=2, sticky="NSEW")
rp_scale.grid(row=3, column=3, columnspan=2, sticky="NSEW")
av_delay_scale.grid(row=4, column=3, columnspan=2, sticky="NSEW")
msr_scale.grid(row=5, column=3, columnspan=2, sticky="NSEW")
act_thresh_scale.grid(row=6, column=3, columnspan=2, sticky="NSEW")
react_t_scale.grid(row=7, column=3, columnspan=2, sticky="NSEW")
res_fact_scale.grid(row=8, column=3, columnspan=2, sticky="NSEW")
rec_t_scale.grid(row=9, column=3, columnspan=2, sticky="NSEW")


#AOO nominal values
lrl_scale.set(60)
url_scale.set(120)
a_amp_scale.set(5000)
v_amp_scale.set(5000)
pw_scale.set(1)
a_sensi_scale.set(0)
v_sensi_scale.set(0)
rp_scale.set(250)
av_delay_scale.set(150)
msr_scale.set(300)
act_thresh_scale.set(4)
react_t_scale.set(30)
res_fact_scale.set(8)
rec_t_scale.set(300)

params.lrl =lrl_scale.get()
params.url =url_scale.get()
params.a_amp =a_amp_scale.get()
params.v_amp =v_amp_scale.get()
params.pw =pw_scale.get()
params.a_sensi =a_sensi_scale.get()
params.v_sensi =v_sensi_scale.get()
params.rp =rp_scale.get()
params.av_delay =av_delay_scale.get()
params.msr =msr_scale.get()
params.act_thresh =act_thresh_scale.get()
params.react_t =react_t_scale.get()
params.res_fact =res_fact_scale.get()
params.rec_t =rec_t_scale.get()

#print(params.save())


att = LabelFrame(canvas_interface, text="Attributes", bg="white", fg="#990000", font = fontStyle5, height=419, width=335, labelanchor=N, relief=RAISED)

#Display parameter values
lrl_att = Label(att, text="Lower Rate:", font=fontStyle9, bg="white")
url_att = Label(att, text="Upper Rate:", font=fontStyle9, bg="white")
a_amp_att = Label(att, text="Atrial Amplitude:", font=fontStyle9, bg="white")
v_amp_att =  Label(att, text="Ventricular Amplitude:", font=fontStyle9, bg="white")
pw_att =  Label(att, text="Pulse Width:", font=fontStyle9, bg="white")
a_sensi_att = Label(att, text="Atrial Sensitivity:", font=fontStyle9, bg="white")
v_sensi_att = Label(att, text="Ventricular Sensitivity:", font=fontStyle9, bg="white")
rp_att = Label(att, text="A/V Refractory Period:", font=fontStyle9, bg="white")
av_delay_att =  Label(att, text="A/V Delay:", font=fontStyle9, bg="white")
msr_att =  Label(att, text="Maximum Sensor Rate:", font=fontStyle9, bg="white")
act_thresh_att = Label(att, text="Activity Threshold:", font=fontStyle9, bg="white")
react_t_att = Label(att, text="Reaction Time:", font=fontStyle9, bg="white")
res_fact_att = Label(att, text="Response Factor:", font=fontStyle9, bg="white")
rec_t_att =  Label(att, text="Recovery Time:", font=fontStyle9, bg="white")

lrl_val = Label(att, textvariable=str(params.lrl), font=fontStyle9, bg="white", fg="#990000", width=4, relief=RIDGE)
url_val = Label(att, textvariable=str(params.url), font=fontStyle9, bg="white", fg="#990000", width=4, relief=RIDGE)
a_amp_val = Label(att, textvariable=str(params.a_amp), font=fontStyle9, bg="white", fg="#990000", width=4, relief=RIDGE)
v_amp_val =  Label(att, textvariable=str(params.v_amp), font=fontStyle9, bg="white", fg="#990000", width=4, relief=RIDGE)
pw_val =  Label(att, textvariable=str(params.pw), font=fontStyle9, bg="white", fg="#990000", width=4, relief=RIDGE)
a_sensi_val = Label(att, textvariable=str(params.a_sensi), font=fontStyle9, bg="white", fg="#990000", width=4, relief=RIDGE)
v_sensi_val = Label(att, textvariable=str(params.v_sensi), font=fontStyle9, bg="white", fg="#990000", width=4, relief=RIDGE)
rp_val = Label(att, textvariable=str(params.rp), font=fontStyle9, bg="white", fg="#990000", width=4, relief=RIDGE)
av_delay_val =  Label(att, textvariable=str(params.av_delay), font=fontStyle9, bg="white", fg="#990000", width=4, relief=RIDGE)
msr_val =  Label(att, textvariable=str(params.msr), font=fontStyle9, bg="white", fg="#990000", width=4, relief=RIDGE)
act_thresh_val = Label(att, textvariable=str(params.act_thresh), font=fontStyle9, bg="white", fg="#990000", width=4, relief=RIDGE)
react_t_val = Label(att, textvariable=str(params.react_t), font=fontStyle9, bg="white", fg="#990000", width=4, relief=RIDGE)
res_fact_val = Label(att, textvariable=str(params.res_fact), font=fontStyle9, bg="white", fg="#990000", width=4, relief=RIDGE)
rec_t_val =  Label(att, textvariable=str(params.rec_t), font=fontStyle9, bg="white", fg="#990000", width=4, relief=RIDGE)




att.grid(row=3, column=5, rowspan=7, columnspan=2, sticky="NSEW")

lrl_att.grid(row=0, column=0, sticky="W")
url_att.grid(row=1, column=0, sticky="W")
a_amp_att.grid(row=2, column=0, sticky="W")
v_amp_att.grid(row=3, column=0, sticky="W")
pw_att.grid(row=4, column=0, sticky="W")
a_sensi_att.grid(row=5, column=0, sticky="W")
v_sensi_att.grid(row=6, column=0, sticky="W")
rp_att.grid(row=7, column=0, sticky="W")
av_delay_att.grid(row=8, column=0, sticky="W")
msr_att.grid(row=9, column=0, sticky="W")
act_thresh_att.grid(row=10, column=0, sticky="W")
react_t_att.grid(row=11, column=0, sticky="W")
res_fact_att.grid(row=12, column=0, sticky="W")
rec_t_att.grid(row=13, column=0, sticky="W")

lrl_val.grid(row=0, column=1, sticky="W")
url_val.grid(row=1, column=1, sticky="W")
a_amp_val.grid(row=2, column=1, sticky="W")
v_amp_val.grid(row=3, column=1, sticky="W")
pw_val.grid(row=4, column=1, sticky="W")
a_sensi_val.grid(row=5, column=1, sticky="W")
v_sensi_val.grid(row=6, column=1, sticky="W")
rp_val.grid(row=7, column=1, sticky="W")
av_delay_val.grid(row=8, column=1, sticky="W")
msr_val.grid(row=9, column=1, sticky="W")
act_thresh_val.grid(row=10, column=1, sticky="W")
react_t_val.grid(row=11, column=1, sticky="W")
res_fact_val.grid(row=12, column=1, sticky="W")
rec_t_val.grid(row=13, column=1, sticky="W")



set_butt = Button(att, text = "Accept Values", font = fontStyle3, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000", command=save)

set_butt.grid(row=14, column=0, rowspan=2, columnspan=2, sticky="NSEW")

att.grid_columnconfigure(0, weight=7)
att.grid_columnconfigure(1, weight=1)

root.mainloop() 