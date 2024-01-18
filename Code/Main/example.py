from implementation import connect, compile_packet

beep = True
id = 4
message = "SOLO FSW"

vuams = connect()
packet = compile_packet(beep, id, message)
vuams.write(packet)