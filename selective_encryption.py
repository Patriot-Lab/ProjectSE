import os
import numpy as np
from dwt import dwt2d, idwt2d
from utils import aes_encrypt, aes_decrypt, sha256_with_key, sha512_with_key, xor_with_sha_key, time_it

@time_it
def encrypt(file_path, buffer,sha_key_str, aes_key, save_data):    
    chunk_size = buffer * buffer
    sha_key = sha_key_str.encode()
    ll2_enc_key = aes_key
    d_private_fragment = []
    d_public_protected_fragment_1 = []
    d_public_protected_fragment_2 = []
    itr_count = 0
        
    with open(file_path, 'rb') as file:
        while True:
            
            chunk = file.read(chunk_size)

            if not chunk:
                break
            print(f'itr_count: {itr_count}')
            itr_count+=1
            
            if len(chunk) < chunk_size:
                chunk += b'\x00' * (chunk_size - len(chunk))
            
            encrypted_ll2, PPF1_XOR, PPF2_XOR = _se_encrypt(chunk=chunk, buffer=buffer, sha_key=sha_key, ll2_enc_key=ll2_enc_key)

            #Step 8, Append to Data Sequence
            d_private_fragment.append(np.frombuffer(encrypted_ll2, dtype=np.uint8))
            d_public_protected_fragment_1.append(np.frombuffer(PPF1_XOR, dtype=np.uint8))
            d_public_protected_fragment_2.append(np.frombuffer(PPF2_XOR, dtype=np.uint8))
    
    if(save_data):
            np.save(f'{file_path[:file_path.rfind("/")]}/enc/{file_path.split("/")[-1]}_PF.npy', np.array(d_private_fragment))
            np.save(f'{file_path[:file_path.rfind("/")]}/enc/{file_path.split("/")[-1]}_PPF_1.npy', np.array(d_public_protected_fragment_1))
            np.save(f'{file_path[:file_path.rfind("/")]}/enc/{file_path.split("/")[-1]}_PPF_2.npy', np.array(d_public_protected_fragment_2))

@time_it
def _get_2d_array(chunk, buffer):
    return np.reshape(np.frombuffer(chunk, dtype=np.uint8), (buffer, buffer))

@time_it
def _se_encrypt(chunk, buffer, sha_key, ll2_enc_key):
    # byte_array = np.frombuffer(chunk, dtype=np.uint8)
    byte_array_2d = _get_2d_array(chunk=chunk, buffer=buffer)
    
    #Step 1, 2D DWT LVL 1
    ll, hl, lh, hh = dwt2d(byte_array_2d)

    #Step 2, 2D DWT LVL 2
    ll2, hl2, lh2, hh2 = dwt2d(ll)

    #Step 3, SHA-256 with key, on ll2, for PPF1
    SHA256_PPF1 = sha256_with_key(sha_key, ll2.tobytes())
    
    #Step 4, SHA-512 with key, on (lh2, hl2, hh2), for PPF2
    SHA512_PPF2 = sha512_with_key(sha_key, np.array([lh2,hl2,hh2]).tobytes())        
    
    #Step 5, PPF1 generation, XOR using generated SHA-256 from ll2
    PPF1_bytes = np.array([hl2, lh2, hh2]).tobytes()
    PPF1_XOR = xor_with_sha_key(PPF1_bytes, SHA256_PPF1)
    
    #Step 6, PPF2 generation, XOR using generated SHA-512 from (lh2, hl2, hh2)
    PPF2_bytes = np.array([hl, lh, hh]).tobytes()
    PPF2_XOR = xor_with_sha_key(PPF2_bytes, SHA512_PPF2)
                
    
    #Step 7, Encrypt LL2 (AES 256)
    encrypted_ll2 = aes_encrypt(ll2.tobytes(), ll2_enc_key)

    return encrypted_ll2, PPF1_XOR, PPF2_XOR

@time_it
def decrypt(file_PF, file_PPF_1, file_PPF_2, buffer, output_file_path, sha_key_str, aes_key):
    
    sha_key = sha_key_str.encode()
    ll2_enc_key = aes_key

    d_private_fragment = np.load(file_PF)
    d_public_protected_fragment_1 = np.load(file_PPF_1)
    d_public_protected_fragment_2 = np.load(file_PPF_2)

    
    with open(output_file_path, 'wb') as file:
        for i in range(len(d_private_fragment)):
            
            #Step 1, get the LL2 from encrypted private fragment
            ll2_dec = aes_decrypt(d_private_fragment[i].tobytes(), ll2_enc_key)
            ll2 = np.frombuffer(ll2_dec, dtype=np.uint8).reshape(int(buffer/4), int(buffer/4))

            #Step 2, Get PPF1
            sha256_ppf1 = sha256_with_key(sha_key, ll2.tobytes())
            ppf1_bytes = xor_with_sha_key(d_public_protected_fragment_1[i].tobytes(), sha256_ppf1)
            ppf1 = np.frombuffer(ppf1_bytes, dtype=np.uint8)
            hl2, lh2, hh2 = np.split(ppf1, 3)
            hl2 = hl2.reshape(int(buffer/4), int(buffer/4))
            lh2 = lh2.reshape(int(buffer/4), int(buffer/4))
            hh2 = hh2.reshape(int(buffer/4), int(buffer/4))
            
            #Step 3, Get PPF2
            sha512_ppf2 = sha512_with_key(sha_key, np.array([lh2,hl2,hh2]).tobytes())        
            ppf2_bytes = xor_with_sha_key(d_public_protected_fragment_2[i].tobytes(), sha512_ppf2)
            ppf2 = np.frombuffer(ppf2_bytes, dtype=np.uint8)
         
            hl, lh, hh = np.split(ppf2, 3)
            hl = hl.reshape(int(buffer/2), int(buffer/2))
            lh = lh.reshape(int(buffer/2), int(buffer/2))
            hh = hh.reshape(int(buffer/2), int(buffer/2))
            
            #Step 4, Get ll
            ll = idwt2d(ll2, hl2, lh2, hh2)
            
            #Step 5, Get original chunk
            byte_array_2d = idwt2d(ll, hl, lh, hh)
            chunk = byte_array_2d.reshape(-1)
            
            if i==len(d_private_fragment)-1:
                chunk = np.trim_zeros(chunk, 'b')
            
            file.write(chunk.tobytes())

