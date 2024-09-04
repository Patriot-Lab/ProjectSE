#Util Functions
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


def bytes_to_bits(b):
    return ''.join([bin(byte)[2:].zfill(8) for byte in bytearray(b)])


def bits_to_bytes_v2(b, chunk_size=8):
    return bytes([int(''.join(b[i:i+chunk_size]), 2) for i in range(0, len(b), chunk_size)])

def sha256_with_key(key, data):
    combined = key + data
    sha256_obj = hashlib.sha256()
    sha256_obj.update(combined)
    return sha256_obj.hexdigest()


def sha512_with_key(key, data):
    combined = key + data
    sha512_obj = hashlib.sha512()
    sha512_obj.update(combined)
    return sha512_obj.hexdigest()

# def xor_with_sha_key(data, sha_hex):
#     sha_bytes = bytes.fromhex(sha_hex)
#     xor_result = bytes([b1 ^ b2 for b1, b2 in zip(data, sha_bytes)])
#     return xor_result

def xor_with_sha_key(data, sha_hex):
    sha_bytes = bytes.fromhex(sha_hex)
    sha_length = len(sha_bytes)
    extended_sha_bytes = sha_bytes * (len(data) // sha_length) + sha_bytes[:len(data) % sha_length]
    xor_result = bytes([b1 ^ b2 for b1, b2 in zip(data, extended_sha_bytes)])
    return xor_result


def recover_data_from_xor(xor_data, sha_hex):
    sha_bytes = bytes.fromhex(sha_hex)
    recovered_data = bytes([b ^ sha_bytes[i] for i, b in enumerate(xor_data)])
    return recovered_data


def aes_encrypt(data, key):
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    return iv + encrypted_data


def aes_decrypt(encrypted_data, key):
    iv = encrypted_data[:16]
    encrypted_data = encrypted_data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted_data

