
import serial
import time
from quiz import start_quiz
# Change this to your Arduino port and baud rate
ARDUINO_PORT = "COM13"   # e.g., "COM3" on Windows or "/dev/ttyACM0" on Linux/Mac
BAUD_RATE = 9600

def check_arduino_connection():
    try:
        # Try connecting to Arduino
        ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=2)
        time.sleep(2)  # Wait for Arduino to reset and send data

        # Send a handshake command
        ser.write(b'ping\n')
        reply = ser.readline().decode().strip()
        ser.close()

        if reply:
            return True, reply
        else:
            return False, None
    except Exception as e:
        print(f"Error: {e}")
        return False, None


def go_to_next_screen(root):
    connected, reply = check_arduino_connection()

    if connected:
        print("Connected")
        start_quiz(root)



