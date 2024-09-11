import os
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from utils import time_it
import oqs


KEY_SIZE = 32
BLOCK_SIZE = AES.block_size


@time_it
def encrypt_message(message, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    padded_message = message + (BLOCK_SIZE - len(message) % BLOCK_SIZE) * b' '
    
    ciphertext = cipher.encrypt(padded_message)
    
    return base64.b64encode(iv + ciphertext)


def encrypt_file(input_file, output_file, key):
    iv = get_random_bytes(BLOCK_SIZE)
    
    with open(input_file, 'rb') as f_in:
        plaintext = f_in.read()
    
    encrypted_data = encrypt_message(plaintext, key, iv)
    
    with open(output_file, 'wb') as f_out:
        f_out.write(encrypted_data)


def encrypt_images_folder(key):
    input_folder = 'images/'
    output_folder = 'images/enc/'
    
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)



    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        
        
        if os.path.isfile(input_path):
            output_path = os.path.join(output_folder, filename + '.enc')
            encrypt_file(input_path, output_path, key)
            print(f"Encrypted {filename} -> {filename}.enc")

kem = "ML-KEM-1024"
with oqs.KeyEncapsulation(kem) as receiver:
    with oqs.KeyEncapsulation(kem) as sender:
        public_key_receiver = receiver.generate_keypair()
        cipher, secret = sender.encap_secret(public_key_receiver)
        encrypt_images_folder(secret)

