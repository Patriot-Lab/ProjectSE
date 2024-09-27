import oqs
import os
from utils import time_it
from pq_sign_util import sign_image, verify_image_signature

def process_images_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image_path = os.path.join(folder_path, filename)
            signature_path = f"keys/{filename}_signature.sig"
            public_key_path = f"keys/{filename}_public_key.pub"
            
            print(f"Signing file: {filename}")
            sign_image(image_path, signature_path, public_key_path)
            
            print(f"Verifying signature for file: {filename}")
            is_valid = verify_image_signature(image_path, signature_path, public_key_path)
            print(f"Signature for {filename} is {'valid' if is_valid else 'invalid'}!\n")

folder_path = 'images'
os.makedirs("keys", exist_ok=True)
process_images_in_folder(folder_path)
