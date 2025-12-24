from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

KEY_FILE = "master.key"

def load_key():
    if not os.path.exists(KEY_FILE):
        key = get_random_bytes(32)  # AES-256
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    return open(KEY_FILE, "rb").read()

def encrypt_file(data):
    key = load_key()
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return cipher.nonce + tag + ciphertext

def decrypt_file(data):
    key = load_key()
    nonce = data[:16]
    tag = data[16:32]
    ciphertext = data[32:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)
