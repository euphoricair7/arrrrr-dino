import socket
import ssl
import serial

global decoded_line
def read_uid_from_arduino():
    global decoded_line
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        ser.flush()

        while True:
            if ser.in_waiting > 0:
                raw_line = ser.readline().strip()
                try:
                    decoded_line = raw_line.decode('utf-8', errors='ignore')
                    print(f"Raw line from serial: {decoded_line}")
                    
                    if decoded_line.startswith(("1","2","3","4","5","6","7","8","9")) :
                        uid = decoded_line[0::]
                        print(f"--uid--")
                        return uid
                except UnicodeDecodeError:
                    print("Failed to decode line as UTF-8")

    except serial.SerialException as e:
        print(f"Serial Exception: {str(e)}")
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
    

uid = read_uid_from_arduino()
if uid:
    print(f"Final UID: {uid}")
else:
    print("No UID read")


#server code

def create_tls_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8443))
    server_socket.listen(5)
  
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    
    print("Server listening on port 8443...")

    while True:
        client_socket, addr = server_socket.accept()

        print(f"Connection from {addr}")

        tls_client_socket=context.wrap_socket(client_socket, server_side=True)
            
        uidb = uid.encode("utf-8")
        tls_client_socket.send(uidb)
        print(f"Sent message: {uid}")

        tls_client_socket.close()


create_tls_server()
