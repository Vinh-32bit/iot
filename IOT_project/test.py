import serial
import time

arduino_port = 'COM8'  
baud_rate = 9600  

try:
    arduino = serial.Serial(arduino_port, baud_rate)
    print("Connected to Arduino")
except serial.SerialException as e:
    print(f"Error: {e}")