import socket
import ssl

def create_tls_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8443))
    server_socket.listen(5)
  
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    
    print("Server listening on port 8443...")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")

            with context.wrap_socket(client_socket, server_side=True) as tls_client_socket:
                
                message = "Hello from TLS server"
                tls_client_socket.send(message.encode('utf-8'))
                print(f"Sent message: {message}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        server_socket.close()

if __name__ == "__main__":
    create_tls_server()
