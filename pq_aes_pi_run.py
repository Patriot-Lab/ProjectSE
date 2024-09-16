import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from utils import time_it

@time_it
def encrypt_file(file_path, output_folder, key):
	with open(file_path, 'rb') as f:
		file_data = f.read()
		iv, encrypted_data = encrypt_data(file_data, key)
		file_name = os.path.basename(file_path)
		output_path = os.path.join(output_folder, file_name + ".enc")
		write_data(iv, output_path, encrypted_data)

@time_it
def encrypt_data(file_data, key):
	iv = get_random_bytes(16)
	cipher = AES.new(key, AES.MODE_CBC, iv)
	encrypted_data = cipher.encrypt(pad(file_data, AES.block_size))
	return (iv, encrypted_data)

@time_it
def write_data(iv, output_path, encrypted_data):
	with open(output_path, 'wb') as f_enc:
		f_enc.write(iv + encrypted_data)

def encrypt_folder(source_folder, output_folder, key):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    files = [file for file in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, file))]

    for file in files:
        file_path = os.path.join(source_folder, file)
        print(f'{file_path}')
        encrypt_file(file_path, output_folder, key)


source_folder = 'images'
output_folder = 'images/enc_aes_256'

key = get_random_bytes(32)

print(f"Generated AES-256 key: {key.hex()}")
encrypt_folder(source_folder, output_folder, key)
