import os
import time
from quiz import start_quiz

# Optional: only import serial when not skipping
try:
    import serial
except ImportError:
    serial = None

# Change this to your Arduino port and baud rate
ARDUINO_PORT = "COM13"   # e.g., "COM3" on Windows or "/dev/ttyACM0" on Linux/Mac
BAUD_RATE = 9600


def check_arduino_connection():
    # If SKIP_SERIAL=1 is set, bypass connection
    if os.getenv("SKIP_SERIAL") == "1":
        print("⚙️  SKIP_SERIAL enabled — skipping Arduino check.")
        return True, "bypassed"

    if serial is None:
        print("⚠️  Serial module not available — skipping Arduino check.")
        return True, "bypassed"

    try:
        ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=2)
        time.sleep(2)  # Wait for Arduino reset and response

        ser.write(b'ping\n')
        reply = ser.readline().decode().strip()
        ser.close()

        if reply:
            return True, reply
        else:
            return False, None
    except Exception as e:
        print(f"⚠️  Serial error: {e}")
        return False, None


def go_to_next_screen(root, subject, chapter):
    connected, reply = check_arduino_connection()

    if connected:
        print("✅ Connected or bypassed — starting quiz.")
        start_quiz(root, subject, chapter)
    else:
        print("❌ Could not connect — skipping to quiz anyway.")
        start_quiz(root, subject, chapter)