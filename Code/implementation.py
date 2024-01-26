#%% Imports and serial connection

import serial # Note this is the pyserial toolbox
from serial.tools.list_ports import comports
import binascii
from time import sleep

VID = "0403"
PID = "6001"
SERIAL_NUMBER = "12345678A"

def connect(VID="0403", PID="6001", SERIAL_NUMBER="12345678A"):
    matching = list()
    for port, desc, hwid in comports():
        if f"USB VID:PID={VID}:{PID}" in hwid and f"SER={SERIAL_NUMBER}" in hwid:
            matching.append(port)
    
    if len(matching) == 0:
        raise ConnectionError("No VU-AMS devices found.")
    elif len(matching) > 1:
        for port, desc, hwid in comports():
            if port in matching:
                print(port, desc, hwid)
        choice = input("Please enter the COM port you want to connect with.")
        try:
            ser = serial.Serial(choice, 38400, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
        except:
            print(f"{choice} was not a valid choice. Aborting.")
            raise ConnectionError("Something went wrong while connecting to the VU-AMS.")
    else:
        ser = serial.Serial(matching[0], 38400, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
    return ser

def start_recording(vuams_serial):
    START = [0x08, 0x00, 0x0B, 0x05, 0xB7, 0xDA, 0x6E, 0x77]
    vuams_serial.write(START)
    sleep(3) # force a sleep to allow device to start

def stop_recording(vuams_serial):
    STOP = [0x08, 0x00, 0x0B, 0x06, 0x0D, 0x8B, 0x67, 0xEE]
    vuams_serial.write(STOP)
        
#%% Header

HEADER = [0x38, 0x00, 0x0E, 0x00, 0x03, 0x00, 0x30, 0x00, 0xFF, 0xFF, 0xFF, 0xFF]

#%% Beeping
def beeping(beep = True):
    if beep:
        return [0x01, 0x00, 0x00, 0x00]
    elif not beep:
        return [0x00, 0x00, 0x00, 0x00]

#%% ID
def hex_id(id):
    if id > 2**32 - 1:
        raise ValueError("ID too large for an unsigned int32")
    byte_id = bytearray(id.to_bytes(4, "little", signed=False))
    return list(byte_id)

#%% String
def hex_string(message):
    if len(message) > 32:
        raise ValueError("Message too large. Maximum is 32 characters.")
    msg = [ord(c) for c in message]
    while len(msg) != 32:
         msg.append(0)
    return (msg)

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

    if len(calc_checksum) % 2 == 0:
        reversed_checksum = list(bytearray.fromhex(calc_checksum))[::-1]
    else:
        reversed_checksum = list(bytearray.fromhex("0" + calc_checksum))[::-1]
    checksum = [hex(x)[2:] for x in reversed_checksum]
    
    return [int(x, 16) for x in checksum]


# %% Create packet
def compile_packet(beep=False, id=1, message="SOLO FSW"):
    marker_beep = beeping(beep)
    marker_id = hex_id(id)
    marker_string = hex_string(message)
    checksum = calc_checksum(bytearray([*HEADER, *marker_beep, *marker_id, *marker_string]))
    return bytearray([*HEADER, *marker_beep, *marker_id, *marker_string, *checksum])

#%%

if __name__ == "__main__":
    ser = connect()
    packet = compile_packet(True, id=4, message="SOLO FSW")
    start_recording(ser)
    sleep(1)
    ser.write(packet)
    sleep(10)
    ser.write(packet)
    sleep(1)
    stop_recording(ser)
    ser.close()
