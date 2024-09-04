from selective_encryption import encrypt
from utils import time_it
from quantcrypt.kem import Kyber
import os

kem = Kyber()
public_key, secret_key = kem.keygen()
cipher_text, shared_secret = kem.encaps(public_key)
sha_key_str = 'Tuesday Evening'

buffer_sizes = list(range(128, 8193, 128))  # Buffer sizes from 128 to 8192 with an interval of 128

folder_path = 'images'

def process_files(folder_path, buffer_sizes, sha_key_str, shared_secret):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            print(f'File: {filename}')
            file_path = os.path.join(folder_path, filename)
            for buffer_size in buffer_sizes:
                print(f'Buffer: {buffer_size}')
                encrypt(file_path=file_path,
                        sha_key_str=sha_key_str,
                        buffer=buffer_size,
                        aes_key=shared_secret)
                
process_files(folder_path, buffer_sizes, sha_key_str, shared_secret)
