#%% Imports and serial connection

import serial
from serial.tools.list_ports import comports
import re
import binascii

for port, desc, hwid in comports():
    if re.match("USB VID:PID=0403:6001", hwid):  # TODO: Change to vendor id?
        ser = serial.Serial(port, 38400, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
        


header = [0x38, 0x00, 0x0E, 0x00, 0x03, 0x00, 0x30, 0x00, 0xFF, 0xFF, 0xFF, 0xFF]
type = [0x01, 0x00, 0x00, 0x00]
beep = [0x04, 0x00, 0x00, 0x00]
marker_string = [0x44, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] 
packet = bytearray([*header, *type, *beep, *marker_string])

def add_checksum(packet):
    hex_data = [hex(x) for x in packet]
    for i, x in enumerate(hex_data):
        if len(x) <= 3:
            hex_data[i] = '0' + x[-1]
        else:
            hex_data[i] = x[-2:]
            
    b = b''.join((binascii.unhexlify(i) for i in hex_data))
    calc_checksum = hex(binascii.crc32(b))[2:]

    reversed_checksum = list(bytearray.fromhex(calc_checksum))[::-1]
    checksum = [hex(x)[2:] for x in reversed_checksum]

    return bytearray([*header, *type, *beep, *marker_string, *[int(x, 16) for x in checksum]])
        
packet = add_checksum(packet)

#%%
ser.write(packet)
