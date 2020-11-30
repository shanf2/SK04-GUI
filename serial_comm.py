import serial as sr
import time

#Initialize the serial communication
def init_serial(ser):
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
    return compare