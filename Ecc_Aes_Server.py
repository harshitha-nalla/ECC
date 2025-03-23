import socket
import random
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

a1, b1, m1 = 2, 3, 17
a2, b2, m2 = 5, 7, 23

public_point = (5, 1)

def mod_inverse(n, m):
    return pow(n, -1, m)

def point_addition(P, Q, a, m):
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % m == 0:
        return None
    slope = ((y2 - y1) * mod_inverse(x2 - x1, m)) % m if x1 != x2 else ((3 * x1 * x1 + a) * mod_inverse(2 * y1, m)) % m
    x3 = (slope * slope - x1 - x2) % m
    y3 = (slope * (x1 - x3) - y1) % m
    return x3, y3

def multiplication(k, P, a, m):
    result = None
    temp = P
    for _ in range(k):
        result = point_addition(result, temp, a, m)
    return result

def generate_key(a, m):
    private_key = random.randint(2, m - 1)
    pub_key = multiplication(private_key, public_point, a, m)
    return private_key, pub_key

def shared_key(private_key, pub_key, a, m):
    return multiplication(private_key, pub_key, a, m)

def decrypt(key, encrypted_msg):
    iv = encrypted_msg[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_padded = cipher.decrypt(encrypted_msg[16:])
    return unpad(decrypted_padded, AES.block_size).decode()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 5000))
server_socket.listen(1)
print("Server is running and waiting for connections")

while True:
    conn, addr = server_socket.accept()
    print(f"Connection established with {addr}")

    curve_choice = conn.recv(1024).decode()

    if curve_choice == "1":
        a, b, m = a1, b1, m1
    else:
        a, b, m = a2, b2, m2

    private_key, pub_key = generate_key(a, m)

    conn.sendall(str(pub_key).encode())

    client_pub_key = eval(conn.recv(1024).decode())

    shared_key_point = shared_key(private_key, client_pub_key, a, m)
    print(f"Shared Key as Point: {shared_key_point}")

    encrypted_msg = conn.recv(1024)
    print(f"Encrypted Message Received: {encrypted_msg.hex()}")
    decrypted_msg = decrypt(hashlib.sha256(str(shared_key_point).encode()).digest()[:16], encrypted_msg)
    print(f"Decrypted Message: {decrypted_msg}")

    conn.close()
    print("Connection closed")
