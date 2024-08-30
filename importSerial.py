import serial

def read_uid_from_serial(port='/dev/ttyACM0', baudrate=9600):
    try:
        ser = serial.Serial(port, baudrate)
        ser.flushInput()  # Clear the buffer
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                if line.startswith("UID:"):
                    uid = line.split(":")[1].strip().replace(" ", "")
                    return uid
    except serial.SerialException as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

uid = read_uid_from_serial()
if uid:
    print(f"Read UID: {uid}")
else:
    print("No UID read.")
