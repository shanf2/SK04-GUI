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
VENT_SIG = np.array([]) #ventrical signal
ART_SIG = np.array([])  #artiary signal

root =tk.Tk()
root.title('Heart Pacemaker')
root.geometry("1100x600")

params = P.Parameters()
nominal = params.save(None)
ser =sr.Serial()

#Variables to hold the value of the current sliders to use for displaying the values.
lrlvar = StringVar()
urlvar = StringVar()
aampvar = StringVar()
vampvar = StringVar()
pwvar = StringVar()
asensivar = StringVar()
vsensivar = StringVar()
rpvar = StringVar()
avdelayvar = StringVar()
actthreshvar = StringVar()
reacttvar = StringVar()
resfactvar = StringVar()
rectvar = StringVar()
msrvar = StringVar()
varlist=[ lrlvar, urlvar, aampvar, vampvar, pwvar, asensivar, vsensivar, rpvar\
	    , avdelayvar, actthreshvar, reacttvar, resfactvar, rectvar, msrvar ]

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
    serial_MSR = params.msr

    serial_data = pack('>BBBBBHHHHHHHHBHHB',serial_status,serial_write,serial_mode,serial_LRL,serial_URL,serial_A_Amplitude,
						serial_V_Amplitude,serial_Pulsewidth,serial_A_Sensitivity,serial_V_Sensitivity,serial_Refractory,serial_AV_Delay,
						serial_Activity_Threshold,serial_Reaction_time,serial_Resopnse_factor,serial_Recovery_time,serial_MSR)
	
    ser.write(serial_data)

    ser.close()


def read_data():
    global ser, compare

    if(ser.isOpen()==False):
    	init_serial()

    #ser.reset_input_buffer()
    serial_status = 0x16
    serial_write = 0x22

    serial_data = pack('>BBBddd',serial_status,serial_write,0,0,0,0)

    ser.write(serial_data)

    data_recevied = ser.read(24) #Read from Serial Port

    try:
    	a = unpack('<BBBHHHHHHHBHHH',data_recevied)
    except Exception:
    	a = unpack('<BBBHHHHHHHBHHH',0,0,0,0,0,0,0,0,0,0,0,0,0,0)

    i=0
    for k, v in compare.items():
    	if(k != "uid" and k != "msr"):
    		compare[k] = a[i]
    		i += 1
    ser.close()
'''
    serial_status = 0x16
    serial_write = 0x22
    mode = a[0]
    lrl = a[1]
    url = a[2]
    a_amp = a[3]
    v_amp = a[4]
    pw = a[5]
    a_sensi = a[6]
    v_sensi = a[7]
    rp = a[8]
    av_delay = a[9]
    act_thresh = a[10]
    react_t = a[11]
    res_fact = a[12]
    rec_t  = a[13]
'''
    

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
fontStyle5 = tkFont.Font(family="Times New Roman", size=20, weight="bold")
fontStyle6 = tkFont.Font(family="Times New Roman", size=15, weight="bold")
fontStyle7 = tkFont.Font(family="Times New Roman", size=10)
fontStyle8 = tkFont.Font(family="Blackadder ITC", size=13, weight="bold")
fontStyle9 = tkFont.Font(family="Times New Roman", size=13, weight="bold")
fontStyle10= tkFont.Font(family="Times New Roman", size=10, weight="bold")

#inital username/passwords
USERNAME = ["---"]*10
PASSWORD = []
OID = [None]
LASTMODE=[]

#Fill a list of current users and passwords from the database to be used in the GUI
def populate_users():

	global USERNAME, PASSWORD, OID
	Data = db.conn('Users.db')
	records = db.fetch_users(Data)

	num = len(records)

	#Refresh list if full
	USERNAME.clear()
	PASSWORD.clear()
	OID.clear()
	LASTMODE.clear()
	for x in records:
		USERNAME.append(x[0])
		PASSWORD.append(x[1])
		LASTMODE.append(x[2])
		OID.append(str(x[3]))

	for x in range(10-num):
		USERNAME.append("---")

global canvas_front

#Startup screen includes transitions from all other screens
def frame1():
	Start.place_forget()
	canvas_reg.place_forget()
	canvas_log.place_forget()
	canvas_interface.place_forget()
	canvas_front.place(x = 150, y = 50)
	Pacemaker_sign.place_forget()
	password_entry2.delete(0,END)
	username_entry.delete(0,END)
	password_entry.delete(0,END)

	#Refresh userlist
	populate_users()

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
	
	global USER_ON	#keep track of which user is logged on
	USER_ON = user_number
	username_label2.configure(text = "Username:  " + USERNAME[user_number])
	password_entry2.focus_set()

#Reset the mode buttons, save last mode the user was in and return to login screens
def log_out():
	Data = db.conn('Users.db')
	exec(params.get_mode()+"_mode.configure(relief=RAISED)")
	db.save_mode(Data, params.mode, OID[USER_ON])
	Data.close()	
	frame1()

#Delete a record from database
def delete_user(user_num):
	Data = db.conn('Users.db')
	db.delete(Data, OID[user_num])
	frame1()
	Data.close()

#Register user screen
def Reg():
	canvas_front.place_forget()
	canvas_reg.place(x = 350, y = 50)
	username_entry.focus_set()

#
def reg_username_password():
	Data = db.conn('Users.db')

	#write into the data base
	populate_users()
	if(username_entry.get()!= "" and password_entry.get()!= "" and len(OID)<10):
		db.register(Data, username_entry.get(), password_entry.get(), nominal)		#add entry to database
		
		#Populate a dictionary to fill a database with parameters for each mode
		p_dict=params.save(OID[len(OID)-1])
		for i in range(1,12):
			p_dict["mode"]=i
			db.save_params(Data, p_dict)
		frame1()
	elif(len(OID)>=10):
		reg_wrong.config(text = "Users full!")
	elif(username_entry.get()== "" and password_entry.get()== ""):
		reg_wrong.config(text = "Invalid Entry!")

	#clear input fields
	username_entry.delete(0,END)
	password_entry.delete(0,END)
	Data.close()
	
#Successful login transitions to the user interface screen
def program_frame():
	global connected
	text = password_entry2.get()
	password_entry2.delete(0,END) 					#Clear the entry
	if(text == PASSWORD[USER_ON]):					#Check if the password entered is correct
		canvas_interface.place(x = 50, y = 25)
		Diff_Pacemaker.place(rely = 0.5, relx = 0.2, anchor="center")		#Display if a new pacemaker is connected
		Diff_Pacemaker.after(2500,lambda: Diff_Pacemaker.config(text = ""))
		canvas_log.place_forget()

		populate_users()
		AOO_mode.configure(relief=RAISED)	#ensure correct button is shown as indented
		params.mode=LASTMODE[USER_ON]		#determine last selected mode
		mode_switch(params.get_mode())		#visually change all parameter settings
		init_serial()
	else:
		pass_wrong.config(text="Wrong password, please try again!")
		#print(USERNAME)
		#print(PASSWORD)

#Configure sliders for the different pacing modes. Labels are changed and values are reset to last saved.
def mode_switch(m):
	Data=db.conn('Users.db')

	#Switch button indentation, change parameter mode
	old_mode = params.mode_switch(m)	
	exec(old_mode+"_mode.configure(relief=RAISED)")
	exec(m+"_mode.configure(relief=SUNKEN)")

	#Pull parameters from the database for the current mode
	vals = db.load_params(Data, OID[USER_ON], params.mode)
	params.update(vals)

	#Change scales to reflect new parameters
	for k in vals.keys():
		if(k != 'uid' and k != 'mode'):
			exec("{}_scale.set(params.{})".format(k,k))
	
	#Update scale dict for later use
	for k, v in params.save(OID[USER_ON]).items():
		if(k != 'mode' and k != 'uid'):
			scales[k] = v
	
	#Populate the attribute values to display to the user
	i=0
	for k,v in scales.items():
		if(k != "mode"):
			varlist[i].set(str(v))
			i = i+1
	
	#Disable all sliders temporarily
	for p in params.params_used("DDDR"):
		exec(p+"_scale.configure(state=DISABLED, bg='grey', troughcolor='grey')")

	#Only enable sliders useful in the current mode
	for p in params.params_used(params.get_mode()):
		exec(p+"_scale.configure(state=NORMAL, bg='#80aaff', troughcolor='white')")

	db.save_mode(Data, params.mode, OID[USER_ON])
	Data.close()	
		
#Save current scale values to mode-specified parameters
def save():

	#Tell the user that parameters have been saved
	saveinfo.configure(text="{}'s {} Parameters Have Been Saved".format(USERNAME[USER_ON], params.get_mode()))
	saveinfo.place(relx=0.5, rely=0.5, anchor="center")
	
	#Add correct mode to scales dict tp update all parameters with
	scales["mode"] = params.mode
	params.update(scales)
	p_dict=params.save(OID[USER_ON])	#Ensure values are being saved to the correct user

	#Populate the attribute values to display to the user
	i=0
	for k,v in scales.items():
		if(k != "mode"):
			varlist[i].set(str(v))
			i = i+1
	
	#Update the database with new parameters and last mode selected
	Data = db.conn('Users.db')
	db.save_params(Data, p_dict)
	db.save_mode(Data, params.mode, OID[USER_ON])
	Data.close()
	saveinfo.after(2500, lambda: saveinfo.configure(text="", fg="#990000"))

#Called every time a scale moves tp update the scale dict
def change(val,par):
	global scales
	scales[par]=val

	#ensure the upper limit and lower limit never cross
	if(par=="lrl"):
		lrl_scale.configure(resolution = 1 if(float(lrl_scale.get()) > 49.8 and float(lrl_scale.get()) < 90.2) else 5)
		if lrl_scale.get() > url_scale.get():
			url_scale.set(lrl_scale.get())
	if(par=="url"):
		if lrl_scale.get() > url_scale.get():
			lrl_scale.set(url_scale.get())

def plot_data():
	global ser,new_window,VENT_SIG,ART_SIG,lines,lines2,canvas_egram

	if(ser.isOpen()==False):
		init_serial()

	ser.open()

	serial_status = 0x16
	serial_write = 71

	serial_data = pack('>BBBddd',serial_status,serial_write,0,0,0,0)

	ser.write(serial_data)

	data_recevied = ser.read(24)
	serial_status = 0x16
	serial_write = 98
	serial_data = pack('>BBBddd',serial_status,serial_write,0,0,0,0)

	ser.write(serial_data)

	ser.close()

	try:
		a = unpack('<HHHHHHHHd',data_recevied)
	except Exception:
		a= (0,0,0)
	if(len(VENT_SIG)<100):
		VENT_SIG = np.append(VENT_SIG,float(a[0:3]))
		ART_SIG = np.append(ART_SIG,float(a[4:7]))
	else:
		VENT_SIG[0:98]=VENT_SIG[1:99]
		ART_SIG[0:98] = ART_SIG[1:99]
		VENT_SIG[99]=float(a[1])
		ART_SIG[99]=float(a[0])
	lines.set_xdata(np.arange(0,len(VENT_SIG)))
	lines.set_ydata(VENT_SIG)
	lines2.set_xdata(np.arange(0,len(ART_SIG)))
	lines2.set_ydata(ART_SIG)

	canvas_egram.draw()

	new_window.after(1, plot_data)

def egram():
	global new_window,lines,lines2,canvas_egram
	new_window = tk.Toplevel(root)
	new_window.title("Egram Graph")
	new_window.configure(background = "light blue")
	new_window.geometry("700x500")
	text = tk.Label(new_window,text = "Egram of the Heart",font = fontStyle5, background = "light blue")
	egram_stop_bt = tk.Button(new_window, text = "Close",font = fontStyle6, bg = 'red',command = egram_stop)

	fig = Figure()
	ax1 = fig.add_subplot(2,1,1)
	ax2 = fig.add_subplot(2,1,2)

	ax1.set_title('Ventricle')
	ax1.set_ylabel('mVolt')
	ax1.set_xlim(0, 100)
	ax1.set_ylim(-5,5) 
	ax2.set_title('Atrium')
	ax2.set_xlabel('Time')
	ax2.set_ylabel('mVolt')
	ax2.set_xlim(0, 100)
	ax2.set_ylim(-5,5)
	ax1.grid()
	ax2.grid()
	lines = ax1.plot([], [])[0]
	lines2 = ax2.plot([], [])[0]

	canvas_egram = FigureCanvasTkAgg(fig, master = new_window)
	canvas_egram.get_tk_widget().place(x=10, y=60, width= 680, height = 420)

	canvas_egram.draw()

	text.place(relx=0.4,rely = 0.02)
	egram_stop_bt.place(relx = 0.88, rely = 0.02)

	new_window.after(1, plot_data)

def egram_stop():
	global new_window,ser
	if(ser.isOpen()==False):
		init_serial()

	ser.open()
	serial_status = 0x16
	serial_write = 98
	serial_data = pack('>BBBddd',serial_status,serial_write,0,0,0,0)

	ser.write(serial_data)

	ser.close()
	new_window.destroy()


#USED TO SHOW ALL THE PARAMETER !! BEST TO KEEP THIS FUNCTION AT THE END OF ALL FUNCTIONS
def show():
	print("Show all the users and their passwords")
	print(USERNAME)
	print(PASSWORD)
	print("Parameters:")
	for p, v in params.save(OID[USER_ON]).items():
		print(p, v)
	print("Scales Dictionary:")
	for p, v in scales.items():
		print(p,v)
	


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

#Borders
header = tk.Canvas(canvas_interface, height=20, width=WIDTH-50, bg=CANVAS_BACKGROUND_COLOR, bd=0, highlightthickness=0)
footer = tk.Canvas(canvas_interface, height=20, width=WIDTH-50, bg=CANVAS_BACKGROUND_COLOR, bd=0, highlightthickness=0)
left = tk.Frame(canvas_interface, bg=CANVAS_BACKGROUND_COLOR, width=25, height=HEIGHT-50)
right = tk.Frame(canvas_interface, bg=CANVAS_BACKGROUND_COLOR, width=25, height=HEIGHT-50)
foot_label = tk.Label(header, text = " ", font = fontStyle7, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000")

footer.grid(row=10, column=1, columnspan=6, sticky="NSEW")
left.grid(row=0, column=0, rowspan=11)
right.grid(row=0, column=7, rowspan=11)
header.grid(row=0, column=1, columnspan=6, sticky="NSEW")
foot_label.grid(row=0, column=1, columnspan=6)

#Return to login screen
logout = tk.Button(header, text="Log Out", font=fontStyle7, bg="#990000", fg="#FFFFFF", command = log_out)

logout.place(relx=0.972, rely=0.5, anchor='center')

#Show pacemaker connected status. Check if new device is connected
connected_label = tk.Label(header, text = "Not Connected", font = fontStyle7, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000")
Diff_Pacemaker = tk.Label(header, text = "A New Pacemaker detected", font = fontStyle7, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000")
connected = header.create_oval(100,5,110,15,fill = "red")

connected_label.grid(row=0, column=1, columnspan=6)

#Egram window button
EGRAM_WINDOW = tk.Button(canvas_interface, text = "EGRAM", font = fontStyle6, bg = "#002DA4", fg = "#FFFFFF",command = egram)

EGRAM_WINDOW.grid(row=2, column=6, sticky="NSEW")

#Mode switching buttons
AOO_mode = tk.Button(canvas_interface, text = "AOO", font = fontStyle6, width=12, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000", command = lambda: mode_switch("AOO"), relief=SUNKEN)
VOO_mode = tk.Button(canvas_interface, text = "VOO", font = fontStyle6, width=12, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000", command = lambda: mode_switch("VOO"))
AAI_mode = tk.Button(canvas_interface, text = "AAI", font = fontStyle6, width=12, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000", command = lambda: mode_switch("AAI"))
VVI_mode = tk.Button(canvas_interface, text = "VVI", font = fontStyle6, width=12, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000", command = lambda: mode_switch("VVI"))
DOO_mode = tk.Button(canvas_interface, text = "DOO", font = fontStyle6, width=12, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000", command = lambda: mode_switch("DOO"))
AOOR_mode = tk.Button(canvas_interface, text = "AOOR", font = fontStyle6, width=12, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000", command = lambda: mode_switch("AOOR"))
VOOR_mode = tk.Button(canvas_interface, text = "VOOR", font = fontStyle6, width=12, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000", command = lambda: mode_switch("VOOR"))
AAIR_mode = tk.Button(canvas_interface, text = "AAIR", font = fontStyle6, width=12, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000", command = lambda: mode_switch("AAIR"))
VVIR_mode = tk.Button(canvas_interface, text = "VVIR", font = fontStyle6, width=12, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000", command = lambda: mode_switch("VVIR"))
DOOR_mode = tk.Button(canvas_interface, text = "DOOR", font = fontStyle6, width=12, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000", command = lambda: mode_switch("DOOR"))
DDDR_mode = tk.Button(canvas_interface, text = "DDDR", font = fontStyle6, width=12, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000", command = lambda: mode_switch("DDDR"))

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



#Sliders to change the parameter values
lrl_scale =		   Scale(canvas_interface, orient=HORIZONTAL, width=18, sliderlength="30", label="Lower Rate Limit", font = fontStyle7, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=30, to=175, resolution=1, command=lambda val: change(val, "lrl"))
url_scale =		   Scale(canvas_interface, orient=HORIZONTAL, width=18, sliderlength="30", label="Upper Rate Limit", font = fontStyle7, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=50, to=175, resolution=5, command=lambda val: change(val, "url"))
a_amp_scale =	   Scale(canvas_interface, orient=HORIZONTAL, width=18, sliderlength="30", label="Atrial Amplitude", font = fontStyle7, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=0, to=5000, resolution=100, command=lambda val: change(val, "a_amp"))
v_amp_scale =	   Scale(canvas_interface, orient=HORIZONTAL, width=18, sliderlength="30", label="Ventricular Amplitude", font = fontStyle7, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=0, to=5000, resolution=100, command=lambda val: change(val, "v_amp"))
pw_scale =		   Scale(canvas_interface, orient=HORIZONTAL, width=18, sliderlength="30", label="Pulse Width", font = fontStyle7, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=1, to=30, resolution=1, command=lambda val: change(val, "pw"))
a_sensi_scale =	   Scale(canvas_interface, orient=HORIZONTAL, width=18, sliderlength="30", label="Atrial Sensitivity", font = fontStyle7, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=0, to=5000, resolution=100, command=lambda val: change(val, "a_sensi"))
v_sensi_scale =	   Scale(canvas_interface, orient=HORIZONTAL, width=18, sliderlength="30", label="Ventricular Sensitivity", font = fontStyle7, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=0, to=5000, resolution=100, command=lambda val: change(val, "v_sensi"))
rp_scale =		   Scale(canvas_interface, orient=HORIZONTAL, width=18, sliderlength="30", label="A/V Refractory Period", font = fontStyle7, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=150, to=500, resolution=10, command=lambda val: change(val, "rp"))
av_delay_scale =   Scale(canvas_interface, orient=HORIZONTAL, width=18, sliderlength="30", label="A/V Delay", font = fontStyle7, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=70, to=300, resolution=10, command=lambda val: change(val, "av_delay"))
act_thresh_scale = Scale(canvas_interface, orient=HORIZONTAL, width=18, sliderlength="30", label="Activity Threshold", font = fontStyle7, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=1, to=7, resolution=1, command=lambda val: change(val, "act_thresh"))
react_t_scale =	   Scale(canvas_interface, orient=HORIZONTAL, width=18, sliderlength="30", label="Reaction Time", font = fontStyle7, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=10, to=50, resolution=10, command=lambda val: change(val, "react_t"))
res_fact_scale =   Scale(canvas_interface, orient=HORIZONTAL, width=18, sliderlength="30", label="Response Factor", font = fontStyle7, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=1, to=16, resolution=1, command=lambda val: change(val, "res_fact"))
rec_t_scale =	   Scale(canvas_interface, orient=HORIZONTAL, width=18, sliderlength="30", label="Recovery Time", font = fontStyle7, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=120, to=960, resolution=60, command=lambda val: change(val, "rec_t"))
msr_scale =		   Scale(canvas_interface, orient=HORIZONTAL, width=18, sliderlength="30", label="Maximum Sensor Rate", font = fontStyle7, troughcolor="white", relief=SUNKEN, bg="#80aaff", from_=50, to=175, resolution=5, command=lambda val: change(val, "msr"))

lrl_scale.grid(row=3, column=1, columnspan=2, sticky="NSEW")
url_scale.grid(row=4, column=1, columnspan=2, sticky="NSEW")
a_amp_scale.grid(row=5, column=1, columnspan=2, sticky="NSEW")
v_amp_scale.grid(row=6, column=1, columnspan=2, sticky="NSEW")
pw_scale.grid(row=7, column=1, columnspan=2, sticky="NSEW")
a_sensi_scale.grid(row=8, column=1, columnspan=2, sticky="NSEW")
v_sensi_scale.grid(row=9, column=1, columnspan=2, sticky="NSEW")
rp_scale.grid(row=3, column=3, columnspan=2, sticky="NSEW")
av_delay_scale.grid(row=4, column=3, columnspan=2, sticky="NSEW")
act_thresh_scale.grid(row=5, column=3, columnspan=2, sticky="NSEW")
react_t_scale.grid(row=6, column=3, columnspan=2, sticky="NSEW")
res_fact_scale.grid(row=7, column=3, columnspan=2, sticky="NSEW")
rec_t_scale.grid(row=8, column=3, columnspan=2, sticky="NSEW")
msr_scale.grid(row=9, column=3, columnspan=2, sticky="NSEW")


#AOO nominal values
lrl_scale.set(params.lrl)
url_scale.set(params.url)
a_amp_scale.set(params.a_amp)
v_amp_scale.set(params.v_amp)
pw_scale.set(params.pw)
a_sensi_scale.set(params.a_sensi)
v_sensi_scale.set(params.v_sensi)
rp_scale.set(params.rp)
av_delay_scale.set(params.av_delay)
act_thresh_scale.set(params.act_thresh)
react_t_scale.set(params.react_t)
res_fact_scale.set(params.res_fact)
rec_t_scale.set(params.rec_t)
msr_scale.set(params.msr)

#scales is used to collect the scale values and use them to update parameter values
scales = {"lrl":lrl_scale.get(), "url":url_scale.get(), "a_amp":a_amp_scale.get(), "v_amp":v_amp_scale.get()\
	     , "pw":pw_scale.get(), "a_sensi":a_sensi_scale.get(), "v_sensi":v_sensi_scale.get()\
	     , "rp":rp_scale.get(), "av_delay":av_delay_scale.get(), "act_thresh":act_thresh_scale.get()\
		 , "react_t":react_t_scale.get(), "res_fact":res_fact_scale.get(), "rec_t":rec_t_scale.get(), "msr":msr_scale.get()}


#Display parameter values
att = LabelFrame(canvas_interface, text="Attributes", bg="white", fg="#990000", font = fontStyle5, height=419, width=335, labelanchor=N, relief=RAISED)

lrl_att = Label(att, text="Lower Rate:", font=fontStyle9, bg="white")
url_att = Label(att, text="Upper Rate:", font=fontStyle9, bg="white")
a_amp_att = Label(att, text="Atrial Amplitude:", font=fontStyle9, bg="white")
v_amp_att =  Label(att, text="Ventricular Amplitude:", font=fontStyle9, bg="white")
pw_att =  Label(att, text="Pulse Width:", font=fontStyle9, bg="white")
a_sensi_att = Label(att, text="Atrial Sensitivity:", font=fontStyle9, bg="white")
v_sensi_att = Label(att, text="Ventricular Sensitivity:", font=fontStyle9, bg="white")
rp_att = Label(att, text="A/V Refractory Period:", font=fontStyle9, bg="white")
av_delay_att =  Label(att, text="A/V Delay:", font=fontStyle9, bg="white")
act_thresh_att = Label(att, text="Activity Threshold:", font=fontStyle9, bg="white")
react_t_att = Label(att, text="Reaction Time:", font=fontStyle9, bg="white")
res_fact_att = Label(att, text="Response Factor:", font=fontStyle9, bg="white")
rec_t_att =  Label(att, text="Recovery Time:", font=fontStyle9, bg="white")
msr_att =  Label(att, text="Maximum Sensor Rate:", font=fontStyle9, bg="white")

lrl_val =		 Label(att, textvariable=lrlvar, font=fontStyle9, bg="white", fg="#990000", width=6, relief=RIDGE)
url_val =		 Label(att, textvariable=urlvar, font=fontStyle9, bg="white", fg="#990000", width=6, relief=RIDGE)
a_amp_val =		 Label(att, textvariable=aampvar, font=fontStyle9, bg="white", fg="#990000", width=6, relief=RIDGE)
v_amp_val =		 Label(att, textvariable=vampvar, font=fontStyle9, bg="white", fg="#990000", width=6, relief=RIDGE)
pw_val =		 Label(att, textvariable=pwvar, font=fontStyle9, bg="white", fg="#990000", width=6, relief=RIDGE)
a_sensi_val =	 Label(att, textvariable=asensivar, font=fontStyle9, bg="white", fg="#990000", width=6, relief=RIDGE)
v_sensi_val =	 Label(att, textvariable=vsensivar, font=fontStyle9, bg="white", fg="#990000", width=6, relief=RIDGE)
rp_val =		 Label(att, textvariable=rpvar, font=fontStyle9, bg="white", fg="#990000", width=6, relief=RIDGE)
av_delay_val =	 Label(att, textvariable=avdelayvar, font=fontStyle9, bg="white", fg="#990000", width=6, relief=RIDGE)
act_thresh_val = Label(att, textvariable=actthreshvar, font=fontStyle9, bg="white", fg="#990000", width=6, relief=RIDGE)
react_t_val =	 Label(att, textvariable=reacttvar, font=fontStyle9, bg="white", fg="#990000", width=6, relief=RIDGE)
res_fact_val =	 Label(att, textvariable=resfactvar, font=fontStyle9, bg="white", fg="#990000", width=6, relief=RIDGE)
rec_t_val =		 Label(att, textvariable=rectvar, font=fontStyle9, bg="white", fg="#990000", width=6, relief=RIDGE)
msr_val =		 Label(att, textvariable=msrvar, font=fontStyle9, bg="white", fg="#990000", width=6, relief=RIDGE)

#Populate attribute values
i=0
for p, v in scales.items():
	if((p != "mode") or (p != "uid")):
		varlist[i].set(str(v))
		i = i+1


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
act_thresh_att.grid(row=9, column=0, sticky="W")
react_t_att.grid(row=10, column=0, sticky="W")
res_fact_att.grid(row=11, column=0, sticky="W")
rec_t_att.grid(row=12, column=0, sticky="W")
msr_att.grid(row=13, column=0, sticky="W")

lrl_val.grid(row=0, column=1, sticky="W")
url_val.grid(row=1, column=1, sticky="W")
a_amp_val.grid(row=2, column=1, sticky="W")
v_amp_val.grid(row=3, column=1, sticky="W")
pw_val.grid(row=4, column=1, sticky="W")
a_sensi_val.grid(row=5, column=1, sticky="W")
v_sensi_val.grid(row=6, column=1, sticky="W")
rp_val.grid(row=7, column=1, sticky="W")
av_delay_val.grid(row=8, column=1, sticky="W")
act_thresh_val.grid(row=9, column=1, sticky="W")
react_t_val.grid(row=10, column=1, sticky="W")
res_fact_val.grid(row=11, column=1, sticky="W")
rec_t_val.grid(row=12, column=1, sticky="W")
msr_val.grid(row=13, column=1, sticky="W")


#Save values button
set_butt = Button(att, text = "Accept Values", font = fontStyle3, bg = CANVAS_BACKGROUND_COLOR, fg = "#990000", command=save)
saveinfo = Label(header, text="", font=fontStyle10, fg="#990000", bg=CANVAS_BACKGROUND_COLOR)

set_butt.grid(row=14, column=0, rowspan=2, columnspan=2, sticky="NSEW")

#Adjust row height/column width
for i in range(8):
	if(i==0 or i==7): canvas_interface.grid_columnconfigure(i, weight=1)
	else: canvas_interface.grid_columnconfigure(i, weight=3)
for i in range(11):
	if(i==0 or i==10): canvas_interface.grid_rowconfigure(i, weight=1)
	else: canvas_interface.grid_rowconfigure(i, weight=2)

att.grid_columnconfigure(0, weight=7)
att.grid_columnconfigure(1, weight=1)

root.mainloop() 