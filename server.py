import socket
import pickle
from crypto_utils import generate_kem_keypair, decapsulate_key, decrypt_message
from replay_window import ReplayWindow
from config import SERVER_HOST, SERVER_PORT

def start_server():
    public_key, private_key = generate_kem_keypair()
    replay = ReplayWindow()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen(1)
    print("Server listening...")

    conn, addr = server.accept()
    print("Connected:", addr)

    conn.send(public_key)

    data = pickle.loads(conn.recv(4096))
    ciphertext = data["ciphertext"]
    seq = data["seq"]

    shared_secret = decapsulate_key(ciphertext, private_key)

    if not replay.check_and_update(seq):
        print("Replay attack detected!")
        return

    enc_data = pickle.loads(conn.recv(4096))
    nonce = enc_data["nonce"]
    ciphertext = enc_data["ciphertext"]
    tag = enc_data["tag"]

    message = decrypt_message(shared_secret, nonce, ciphertext, tag)
    print("Secure Message:", message)

    conn.close()

if __name__ == "__main__":
    start_server()