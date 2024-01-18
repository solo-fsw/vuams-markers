#%% Imports and serial connection

import serial
from serial.tools.list_ports import comports
import re
import binascii

for port, desc, hwid in comports():
    if re.match("USB VID:PID=0403:6001", hwid):  # TODO: Change to vendor id?
        ser = serial.Serial(port, 38400, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
        
#%% Header

HEADER = [0x38, 0x00, 0x0E, 0x00, 0x03, 0x00, 0x30, 0x00, 0xFF, 0xFF, 0xFF, 0xFF]

#%% Beeping
def beeping(beep = True):
    if beep:
        return [0x01, 0x00, 0x00, 0x00]
    elif not beep:
        return [0x00, 0x00, 0x00, 0x00]

#%% ID
def hex_id(id=4):
    if id > 2**32 - 1:
        raise ValueError("ID too large for an unsigned int32")
    byte_id = bytearray(id.to_bytes(4, "little", signed=False))
    return list(byte_id)

#%% String
def hex_string(message="4"):
    return [0x44, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]


#%% Checksum
def calc_checksum(packet):
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
    
    return [int(x, 16) for x in checksum]


# %% Create packet
def compile_packet(beep=True, id=4, message=4):
    marker_beep = beeping(beep)
    marker_id = hex_id(id)
    marker_string = hex_string(message)
    checksum = calc_checksum(bytearray([*HEADER, *marker_beep, *marker_id, *marker_string]))
    return bytearray([*HEADER, *marker_beep, *marker_id, *marker_string, *checksum])

packet = compile_packet()

#%%
ser.write(packet)
