import serial as sr
from struct import *
import time

ser = sr.Serial('COM6', baudrate = 115200, bytesize=sr.EIGHTBITS , timeout = 1)
serial_status = 22
serial_write = 34

serial_data = pack('>BBBBBBBBBBBBBBBBBBBBBBBBBB',0x16,0x22,0x01,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20)
print(ser.name)

print("received data: ", serial_data)
ser.write(serial_data)

s = ser.readline()
print("output data: ", s)
#print("output data: ", s.decode())

print(calcsize('>BBBBBHHHHHHHHBHH'))
a = unpack('>BBBBBHHHHHHHHBHH',s)

print(a[0])
print(a)