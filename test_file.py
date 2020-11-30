import serial as sr
from struct import *
import parameters as P
import time

params = P.Parameters()




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

serial_data = pack('>BBBBBHHHHHHHHBHHBB',serial_status,serial_write,serial_mode,serial_LRL,serial_URL,serial_A_Amplitude,
						serial_V_Amplitude,serial_Pulsewidth,serial_A_Sensitivity,serial_V_Sensitivity,serial_Refractory,serial_AV_Delay,
						serial_Activity_Threshold,serial_Reaction_time,serial_Resopnse_factor,serial_Recovery_time,serial_MSR,0)

ser = sr.Serial('COM6', baudrate = 115200, timeout = 1)
print(ser.name)
print("input data: ", serial_data)
print("input data: ", list(serial_data))

print(calcsize('>BBBBBHHHHHHHHBHHBB'))

ser.write(serial_data)

ser.close()
time.sleep(1)

'''
serial_status = 0x16	#22	#0x16
#serial_write = 0x22		#34	#0x22
serial_write = 98 	#0x62
#serial_write = 71  #0x47



serial_data = pack('>BB',serial_status,serial_write)

print("input data size",calcsize('>BB'))
print("input data: ", serial_data)
print("input data: ", list(serial_data))


ser.write(serial_data)
'''
ser.open()

serial_status = 0x16	#22	#0x16
serial_write = 0x22		#34	#0x22
#serial_write = 98 	#0x62
#serial_write = 71  #0x47

#serial_data = pack('>B',serial_write)
serial_data = pack('>BBBddd',serial_status,serial_write,0,0,0,0)

print("input data size",calcsize('>BBBdddB'))
print("input data: ", serial_data)
print("input data: ", list(serial_data))

ser.write(serial_data)

time.sleep(1)

s = ser.read(24)

print("recevied data: ",s)
print("recevied data: ",list(s))

print("recevied data size",calcsize('<BBBHHHHHHHHBHH'))

#a = unpack('<BBBHHHHHHHBHHH',s)

ser.close()
#print(a)
