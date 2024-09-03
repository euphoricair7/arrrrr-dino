



import hashlib
import hmac

from tinyec import registry
import secrets

from tls_client import create_tls_client

import firebase_admin
from firebase_admin import credentials, firestore

# Firebase setup
cred = credentials.Certificate(r'C:/Users/shail/OneDrive/Desktop/proof/rfid-db-5d32b-firebase-adminsdk-dbval-d4136a83f1.json')

firebase_admin.initialize_app(cred)
db = firestore.client()



'''
def on_snapshot(col_snapshot, changes, read_time):
    global uid
    for doc in col_snapshot:
        data = doc.to_dict()
        uid = data.get('uid', 'N/A')
        timestamp = data.get('timestamp', 'N/A')
        print(f"Latest UID: {uid} at {timestamp}")


import re

def extract_uid_from_string(log_entry):
    # Assuming the UID is the part after "Latest UID: " and before " at"
    match = re.search(r'Latest UID: (.*?) at', log_entry)
    if match:
        return match.group(1)
    return None

# Example usage
log_entry = "Latest UID: Card UID: at 2024-08-31 02:41:55.338000+00:00"
uid = extract_uid_from_string(log_entry)
print("Extracted UID:", uid)
     

def main():
    print("Listening for changes in Firebase...")
    
    col_ref = db.collection('rfid_data')
    query = col_ref.order_by('timestamp', direction=firestore.Query.DESCENDING)
    query.on_snapshot(on_snapshot)

    
   
if __name__ == "__main__":
    main()

'''
def compress(pubKey):
    return "{:064x}".format(pubKey.x)

'''
def sha_256(self):
      password_input=self.password_input_5.toPlainText()
        hash_obj=hashlib.sha256()
        hash_obj.update(password_input.encode())
       #self.hashpass=hash_obj.hexdigest()
        print(self.hashpass)

'''

'''
  return hmac.new(
    shared_key.encode("utf-8"),
    #message.encode("utf-8"),
    hashlib.sha256
  ).hexdigest()
'''
'''
import hashlib

def derive_aes(shared_key):
    # Convert the shared key from hexadecimal string to bytes
    #shared_key_bytes = bytes.fromhex(shared_key)

    shared_key_bytes = ''.join([chr(int(shared_key[i:i+2], 16)) for i in range(0, len(shared_key), 2)])


    hash_obj = hashlib.sha256()

    hash_obj.update(shared_key_bytes)

    hashpass = hash_obj.hexdigest()

    return hashpass

shared_key = "0x7b81a3c291c2b5c9694617ae87a51aa0f11ced56e942eff0c1ff41ec5895165f0"
derived_key = derive_aes(shared_key)
print("Derived AES Key:", derived_key)

'''

import hashlib

def derive_aes(shared_key):


    shared_key_bytes = bytes.fromhex(shared_key)

    hash_obj = hashlib.sha256()
    hash_obj.update(shared_key_bytes)
    hashpass = hash_obj.hexdigest()
    return hashpass

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def encrypt_aes(key, plaintext):
    plaintext_bytes = plaintext.encode('utf-8')

    iv = os.urandom(16)


    cipher = Cipher(algorithms.AES(bytes.fromhex(key)), modes.CFB(iv), backend=default_backend())


    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(plaintext_bytes) + encryptor.finalize()
    return iv + ciphertext


def decrypt_aes(key, ciphertext):
    iv = ciphertext[:16]
    actual_ciphertext = ciphertext[16:]

    cipher = Cipher(algorithms.AES(bytes.fromhex(key)), modes.CFB(iv), backend=default_backend())

    decryptor = cipher.decryptor()

    plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()

    return plaintext

curve = registry.get_curve('brainpoolP256r1')

senderPrivKey = secrets.randbelow(curve.field.n)
senderPubKey = senderPrivKey * curve.g
print("Sender public key:", compress(senderPubKey))

recieverPrivKey = secrets.randbelow(curve.field.n)
recieverPubKey = recieverPrivKey * curve.g
print("Reciever public key:", compress(recieverPubKey))

print("Now exchange the public keys (e.g. through Internet)")

senderSharedKey = senderPrivKey * recieverPubKey
#senderSharedKey_x=senderSharedKey.x
sender_compress=compress(senderSharedKey)
print("Sender shared key:", compress(senderSharedKey))

recieverSharedKey = recieverPrivKey * senderPubKey
print("Reciever shared key:", compress(recieverSharedKey))

print("Equal shared keys:", senderSharedKey == recieverSharedKey)



#plaintext is the uid
#print("UID is:", uid)

plaintext = create_tls_client()
print("plaintext:",plaintext)
shakey=derive_aes(sender_compress)
aesKey= encrypt_aes(shakey,plaintext)
ddd = decrypt_aes(shakey,aesKey)

print("SHA256 encrypted key:",shakey)
print("Final encrypted aes implementation:",aesKey)
print("Decrypted: ",ddd)

hex_string = ddd.decode('utf-8').replace(" ", "")

verify = "ENCRYPTED" if senderSharedKey == recieverSharedKey else "INVALID PASS!!!"
print(verify)




#verify="aa 33 44 gg"
import socket
import ssl


def create_tls_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8443))
    server_socket.listen(5)


    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    print("Server listening on port 8443...")

    while True:

        client_socket, addr = server_socket.accept()


        tls_client_socket = context.wrap_socket(client_socket, server_side=True)

        
        print("response is:",verify)
        print(f"Connection from {addr}")
        bytes_data = verify.encode("utf-8")
        tls_client_socket.send(bytes_data)
        tls_client_socket.close()


create_tls_server()
