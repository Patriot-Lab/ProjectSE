#Util Functions
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import time
from numba import njit

def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"{func.__name__}: {end_time - start_time:.9f}") #in seconds
        return result
    return wrapper

@time_it
def bytes_to_bits(b):
    return ''.join([bin(byte)[2:].zfill(8) for byte in bytearray(b)])

@time_it
def bits_to_bytes_v2(b, chunk_size=8):
    return bytes([int(''.join(b[i:i+chunk_size]), 2) for i in range(0, len(b), chunk_size)])



@time_it
def sha256_with_key(key, data):
    combined = key + data
    sha256_obj = hashlib.sha256()
    sha256_obj.update(combined)
    return sha256_obj.hexdigest()

@time_it
def sha512_with_key(key, data):
    combined = key + data
    sha512_obj = hashlib.sha512()
    sha512_obj.update(combined)
    return sha512_obj.hexdigest()

# def xor_with_sha_key(data, sha_hex):
#     sha_bytes = bytes.fromhex(sha_hex)
#     xor_result = bytes([b1 ^ b2 for b1, b2 in zip(data, sha_bytes)])
#     return xor_result

# @time_it
# # @njit
# def xor_with_sha_key(data, sha_hex):
#     sha_bytes = bytes.fromhex(sha_hex)
#     sha_length = len(sha_bytes)
#     extended_sha_bytes = sha_bytes * (len(data) // sha_length) + sha_bytes[:len(data) % sha_length]
#     xor_result = bytes([b1 ^ b2 for b1, b2 in zip(data, extended_sha_bytes)])
#     return xor_result

import numpy as np
from numba import njit

@time_it
@njit
def xor_with_sha_key_numba(data_array, sha_array):
    data_length = len(data_array)
    sha_length = len(sha_array)
    
    # Create an extended SHA bytes array
    extended_sha_array = np.empty(data_length, dtype=np.uint8)
    
    for i in range(data_length):
        extended_sha_array[i] = sha_array[i % sha_length]
    
    # Perform XOR operation
    xor_result = np.bitwise_xor(data_array, extended_sha_array)
    
    return xor_result

@time_it
def xor_with_sha_key(data, sha_hex):
    # Convert hex string to bytes and then to NumPy array
    sha_bytes = np.frombuffer(bytes.fromhex(sha_hex), dtype=np.uint8)
    
    # Convert input data to NumPy array of uint8
    data_array = np.frombuffer(data, dtype=np.uint8)
    
    # Call the Numba-optimized function
    xor_result = xor_with_sha_key_numba(data_array, sha_bytes)
    
    # Convert the result back to bytes
    return xor_result.tobytes()

@time_it
def aes_encrypt(data, key):
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    return iv + encrypted_data

@time_it
def aes_decrypt(encrypted_data, key):
    iv = encrypted_data[:16]
    encrypted_data = encrypted_data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted_data




