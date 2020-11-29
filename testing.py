from struct import *

serial_data = pack('>BBBBBHHHHHHHHBHH',0x16,0x22,1,30,125,3000,1000,2,2500,2400,325,120,3,25,6,250)
print("bigendian   ",serial_data)

serial_data1 = pack('<BBBBBHHHHHHHHBHH',0x16,0x22,1,30,125,3000,1000,2,2500,2400,325,120,3,25,6,250)
print("smallendian ",serial_data1)

print (list(serial_data))
print (list(serial_data1))