import ssl
import socket

def create_tls_client():
    server_address = ('10.7.18.169', 8443)

    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    
    tls_client_socket = context.wrap_socket(client_socket, server_hostname='10.7.18.169')

   
    tls_client_socket.connect(server_address)
    #tls_client_socket.sendall(b"A4 4H 5K 3L")

    
    response = tls_client_socket.recv(1024).decode()
    print(f"Received UID from server 1: {response}")

   
    tls_client_socket.close()

    return response

if __name__ == "__main__":
    create_tls_client()
