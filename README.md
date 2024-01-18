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
