import socket
import pickle
import random
from crypto_utils import encapsulate_key, encrypt_message
from config import SERVER_HOST, SERVER_PORT

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_HOST, SERVER_PORT))

    public_key = client.recv(4096)

    ciphertext, shared_secret = encapsulate_key(public_key)

    seq = random.randint(0, 100000)

    client.send(pickle.dumps({
        "ciphertext": ciphertext,
        "seq": seq
    }))

    nonce, enc_message, tag = encrypt_message(shared_secret, "Hello from Quantum-Safe IoT Device")

    client.send(pickle.dumps({
        "nonce": nonce,
        "ciphertext": enc_message,
        "tag": tag
    }))

    client.close()

if __name__ == "__main__":
    start_client()