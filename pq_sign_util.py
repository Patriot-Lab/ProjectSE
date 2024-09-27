import oqs
from utils import time_it

@time_it
def sign_image(image_path, signature_path, public_key_path):
    with open(image_path, "rb") as image_file:
        file_data = image_file.read()

    with oqs.Signature('Dilithium5') as signer:
        public_key = signer.generate_keypair()
        signature = signer.sign(file_data)

    with open(signature_path, "wb") as sig_file:
        sig_file.write(signature)

    with open(public_key_path, "wb") as pub_file:
        pub_file.write(public_key)

@time_it
def verify_image_signature(image_path, signature_path, public_key_path):
    with open(image_path, "rb") as image_file:
        file_data = image_file.read()

    with open(signature_path, "rb") as sig_file:
        signature_to_verify = sig_file.read()

    with open(public_key_path, "rb") as pub_file:
        public_key_to_verify = pub_file.read()

    with oqs.Signature('Dilithium5') as verifier:
        return verifier.verify(file_data, signature_to_verify, public_key_to_verify)

# Test usage : need to create directories images, keys and need to place landscape.png in images directory
sign_image("data/files/landscape.png", "keys/signature.sig", "keys/public_key.pub")
is_valid = verify_image_signature("data/files/landscape.png", "keys/signature.sig", "keys/public_key.pub")
print("Signature is valid!" if is_valid else "Signature is invalid!")