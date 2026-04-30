import oqs
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from config import KEM_ALGORITHM

def generate_kem_keypair():
    kem = oqs.KeyEncapsulation(KEM_ALGORITHM)
    public_key = kem.generate_keypair()
    private_key = kem.export_secret_key()
    return public_key, private_key

def encapsulate_key(public_key):
    kem = oqs.KeyEncapsulation(KEM_ALGORITHM)
    ciphertext, shared_secret = kem.encap_secret(public_key)
    return ciphertext, shared_secret

def decapsulate_key(ciphertext, private_key):
    kem = oqs.KeyEncapsulation(KEM_ALGORITHM, secret_key=private_key)
    shared_secret = kem.decap_secret(ciphertext)
    return shared_secret

def encrypt_message(key, plaintext):
    cipher = AES.new(key[:32], AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode())
    return cipher.nonce, ciphertext, tag

def decrypt_message(key, nonce, ciphertext, tag):
    cipher = AES.new(key[:32], AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext.decode()