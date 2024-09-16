from selective_encryption import encrypt
import oqs
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

kem = "ML-KEM-1024"
sha_key_str = 'Tuesday Evening'

BLOCK_SIZE = AES.block_size

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
                        aes_key=shared_secret,
                        save_data=True)
            
                
                
                
with oqs.KeyEncapsulation(kem) as receiver:
    with oqs.KeyEncapsulation(kem) as sender:
        public_key_receiver = receiver.generate_keypair()
        cipher, secret = sender.encap_secret(public_key_receiver)
        process_files(folder_path, buffer_sizes, sha_key_str, secret)
