# VU-AMS MARKERS

> A (64-bit) python implementation for sending markers to the vu-ams through a serial connection.

## Usage

For usage of the provided python code, only the `pyserial` library is required. An example environment if provided (`Code\Main\environment.yml`).

Markers can be sent by providing the `compile_packet` function with three parameters, and then sending the marker to the vu-ams over the serial connection. The marker parameters are:

- beep
  - Boolean: decides if the vu-ams should beep upon receiving the marker
- id
  - int32: the marker value
- message
  - string (max 32 characters): an additional remark for the sent marker

Example code for sending marker can be found in the repository (`Code\Main\example.py`).

## Installation

The repository can easily be installed by using the pip package manager. Pip can pull the package straight from git using the following command:

```
pip install git+https://github.com/solo-fsw/vuams-markers.git
```

An example script after installing the package through git would be:

```python
# Import the vuams functions
from vuams_markers import connect, compile_packet

# Connect to the vuams over serial
ser = connect()

# Compile a marker packet
packet = compile_packet(True, id=4, message="SOLO FSW")

# Start the vuams recording
start_recording(ser)

sleep(1)  # Do something

# Send a marker to the vuams
ser.write(packet)

sleep(10)  # Do more things

# Send another marker to the vuams
ser.write(packet)

sleep(1)  # Final action

# Stop the vuams recording
stop_recording(ser)
```

## OpenSesame

This implementation is compatible with OpenSesame 3.3.14 and above.

An example of an OpenSesame task sending vuams markers can be found in the repository (`/Example/OpenSesam/Example_vuams.osexp`).
