import serial as sr
from struct import *
import parameters as P
import time
ser = sr.Serial('COM6', baudrate = 115200, timeout = 1)
time.sleep(1)

serial_status = 0x16	#22	#0x16
serial_write = 0x22		#34	#0x22
#serial_write = 0x62
serial_write = 0x47
serial_data = pack('>BBBddd',serial_status,serial_write,0,0,0,0)
ser.flush()


print("input data size",calcsize('>BB'))
print("input data: ", serial_data)
print("input data: ", list(serial_data))

ser.write(serial_data)

s = ser.read(24)

print("recevied data: ",s)
print("recevied data: ",list(s))
print("recevied data size",calcsize('<BBBHHHHHHHHBHH'))
a = unpack('<BBBHHHHHHHBHHH',s)

ser.close()
print(a)
print(a[0])