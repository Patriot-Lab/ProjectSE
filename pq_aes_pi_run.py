import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from utils import time_it

KEY_SIZE = 32
BLOCK_SIZE = AES.block_size 

@time_it
def encrypt_file(input_file, output_file, key):
    iv = get_random_bytes(BLOCK_SIZE)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    with open(input_file, 'rb') as f_in:
        
        plaintext = f_in.read()
        padded_data = pad(plaintext, BLOCK_SIZE)
    
    ciphertext = cipher.encrypt(padded_data)
    
    with open(output_file, 'wb') as f_out:
        f_out.write(iv + ciphertext)

def encrypt_images_folder():
    input_folder = 'images/'
    output_folder = 'images/enc/'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    key = get_random_bytes(KEY_SIZE)

    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        
        if os.path.isfile(input_path):
            output_path = os.path.join(output_folder, filename + '.enc')
            encrypt_file(input_path, output_path, key)
            print(f"Encrypted {filename} -> {filename}.enc")
    
    return key

if __name__ == '__main__':
    key = encrypt_images_folder()
    print("Encryption complete! AES-256 key (store securely):", key.hex())
