from implementation import connect, compile_packet, start_recording, stop_recording
import time 

beep = True
id = 4
message = "SOLO FSW"

vuams = connect() #c 
start_recording(vuams)
packet = compile_packet(beep, id, message)
vuams.write(packet)
time.sleep(1)
vuams.write(packet)
time.sleep(1)
vuams.write(packet)
stop_recording(vuams)