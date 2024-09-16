from selective_encryption import encrypt
from utils import time_it
import oqs
import os
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

kem = "ML-KEM-1024"
sha_key_str = 'Tuesday Evening'

BLOCK_SIZE = AES.block_size

buffer_sizes = list(range(128, 8193, 128))  # Buffer sizes from 128 to 8192 with an interval of 128

folder_path = 'images'

import os
import base64
from Crypto.Cipher import AES

BLOCK_SIZE = AES.block_size
iv = os.urandom(16)

@time_it
def aes_encrypt_file(input_file_path, output_file_path, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    with open(input_file_path, 'rb') as infile, open(output_file_path, 'wb') as outfile:
        while True:
            chunk = infile.read(BLOCK_SIZE)
            
            if len(chunk) == 0:
                break
            
            if len(chunk) % BLOCK_SIZE != 0:
                padding_length = BLOCK_SIZE - len(chunk) % BLOCK_SIZE
                chunk += bytes([padding_length]) * padding_length
            
            encrypted_chunk = cipher.encrypt(chunk)
            
            outfile.write(encrypted_chunk)


def process_files(folder_path, buffer_sizes, sha_key_str, shared_secret):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            print(f'File: {filename}')
            file_path = os.path.join(folder_path, filename)
            aes_encrypt_file(file_path, f'images/enc/encrypted_output_file.enc', shared_secret, iv)
            for buffer_size in buffer_sizes:
                print(f'Buffer: {buffer_size}')
                encrypt(file_path=file_path,
                        sha_key_str=sha_key_str,
                        buffer=buffer_size,
                        aes_key=shared_secret,
                        save_data=True)
            
                
                
                
with oqs.KeyEncapsulation(kem) as receiver:
    with oqs.KeyEncapsulation(kem) as sender:
        public_key_receiver = receiver.generate_keypair()
        cipher, secret = sender.encap_secret(public_key_receiver)
        process_files(folder_path, buffer_sizes, sha_key_str, secret)
