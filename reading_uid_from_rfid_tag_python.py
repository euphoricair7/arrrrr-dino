import serial

# Replace 'COM3' with the port your Arduino is connected to (e.g., 'COM3' on Windows, '/dev/ttyUSB0' on Linux, or '/dev/ttyACM0' on macOS)
arduino_port = 'COM3' 
baud_rate = 9600  # The baud rate should match the rate in your Arduino sketch

# Establish a connection to the serial port
ser = serial.Serial(arduino_port, baud_rate)

print("Waiting for data...")

try:
    while True:
        if ser.in_waiting > 0:  # Check if there is data in the buffer
            line = ser.readline().decode('utf-8').strip()  # Read and decode the line
            print(f"Received: {line}")  # Print the data received from Arduino
except KeyboardInterrupt:
    print("Exiting the program...")
finally:
    ser.close()  # Close the serial connection when done

# 
