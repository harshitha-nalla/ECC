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

def encrypt(key, msg):
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    encrypted = cipher.encrypt(pad(msg.encode(), AES.block_size))
    return iv + encrypted

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5000))

curve_choice = input("Select Curve 1 or 2: ")
client_socket.sendall(curve_choice.encode())

if curve_choice == "1":
    a, b, m = a1, b1, m1
else:
    a, b, m = a2, b2, m2

private_key, pub_key = generate_key(a, m)

server_pub_key = eval(client_socket.recv(1024).decode())

client_socket.sendall(str(pub_key).encode())

shared_key_point = shared_key(private_key, server_pub_key, a, m)
print(f"Shared Key as Point: {shared_key_point}")

message = input("Enter message to send: ")
encrypted_msg = encrypt(hashlib.sha256(str(shared_key_point).encode()).digest()[:16], message)
print(f"Encrypted Message Sent: {encrypted_msg.hex()}")
client_socket.sendall(encrypted_msg)

client_socket.close()
