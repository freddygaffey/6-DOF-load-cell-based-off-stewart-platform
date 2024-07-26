import serial

try:
    ser = serial.Serial('/dev/ttyUSB0', 230400)
    print("Serial port opened successfully")
except Exception as e:
    print(f"Failed to open serial port: {e}")