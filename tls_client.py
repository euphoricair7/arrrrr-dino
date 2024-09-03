import ssl
import socket
import secrets
from tinyec import registry
import hashlib
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import hmac

# Utility functions
def compress(pubKey):
    return "{:064x}".format(pubKey.x)

def derive_aes(shared_key):
    shared_key_bytes = bytes.fromhex(shared_key)
    hash_obj = hashlib.sha256()
    hash_obj.update(shared_key_bytes)
    return hash_obj.hexdigest()

def encrypt_aes(key, plaintext):
    plaintext_bytes = plaintext.encode('utf-8')
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(bytes.fromhex(key)), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext_bytes) + encryptor.finalize()
    return iv + ciphertext

def hmac_sha256(key, message):
    message_bytes = message.encode("utf-8")
    hmac_obj = hmac.new(key.encode('utf-8'), message_bytes, hashlib.sha256)
    return hmac_obj.hexdigest()

def create_tls_client():
    server_address = ('10.7.18.176', 8443)  # Replace with your server's IP address and port

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # TLS configuration
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    tls_client_socket = context.wrap_socket(client_socket, server_hostname='localhost')

    tls_client_socket.connect(server_address)

    # ECDH key generation for the sender
    curve = registry.get_curve('brainpoolP256r1')
    senderPrivKey = secrets.randbelow(curve.field.n)
    senderPubKey = senderPrivKey * curve.g
    senderPubKey_compressed = compress(senderPubKey)
    print("Sender public key:", senderPubKey_compressed)

    # Send sender's public key to server
    tls_client_socket.sendall(senderPubKey_compressed.encode('utf-8'))

    # Receive receiver's public key
    receiverPubKey_compressed = tls_client_socket.recv(1024).decode('utf-8')
    receiverPubKey = curve.point(int(receiverPubKey_compressed, 16), False)

    # Compute shared key
    senderSharedKey = senderPrivKey * receiverPubKey
    sender_compress = compress(senderSharedKey)
    print("Sender shared key:", sender_compress)

    # Encrypt the plaintext
    plaintext = "83 5A F6 19"
    shared_key = derive_aes(sender_compress)
    ciphertext = encrypt_aes(shared_key, plaintext)
    print("Encrypted data:", ciphertext.hex())

    # Generate HMAC
    hmacHash = hmac_sha256(shared_key, plaintext)
    print("HMAC hash is:", hmacHash)

    # Send ciphertext and HMAC
    tls_client_socket.sendall(ciphertext.hex().encode('utf-8'))
    tls_client_socket.sendall(hmacHash.encode('utf-8'))

    response = tls_client_socket.recv(1024).decode()
    print(f"Received: {response}")

    tls_client_socket.close()

if __name__ == "__main__":
    create_tls_client()
