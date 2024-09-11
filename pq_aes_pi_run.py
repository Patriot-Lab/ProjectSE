import os
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from utils import time_it
from selective_encryption import _se_encrypt
import oqs

KEY_SIZE = 32
BLOCK_SIZE = AES.block_size
BUFFER_SIZE = 3200

@time_it
def encrypt_message(message, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    padded_message = message + (BLOCK_SIZE - len(message) % BLOCK_SIZE) * b' '
    
    ciphertext = cipher.encrypt(padded_message)
    
    return base64.b64encode(iv + ciphertext)


def encrypt_file(input_file, output_file, key):
    iv = get_random_bytes(BLOCK_SIZE)
    
    with open(input_file, 'rb') as f_in:
        chunk = f_in.read(BUFFER_SIZE*BUFFER_SIZE)
        
        if len(chunk) < BUFFER_SIZE:
            chunk = f_in.read()
    
    encrypted_data = encrypt_message(chunk, key, iv)
    
    _se_encrypt(chunk=chunk, buffer=BUFFER_SIZE, sha_key='Tuesday Evening'.encode(), ll2_enc_key=key)
    
    with open(output_file, 'wb') as f_out:
        f_out.write(encrypted_data)


input_file = 'images/4MB_image.png'
output_file = 'images/enc/4MB_image.png.enc'

kem = "ML-KEM-1024"
with oqs.KeyEncapsulation(kem) as receiver:
    with oqs.KeyEncapsulation(kem) as sender:
        public_key_receiver = receiver.generate_keypair()
        cipher, secret = sender.encap_secret(public_key_receiver)
        encrypt_file(input_file, output_file, secret)
        print(f"Encrypted {input_file} -> {output_file}")
