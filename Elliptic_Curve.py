import random
import math
a = 2
b = 3
m = 17
def generate_point(a, b, m):
    while True:
        x = random.randint(1, m - 1)
        y_2 = (pow(x, 3) + a * x + b) % m
        y = math.isqrt(y_2)
        if (y * y) % m == y_2:
            return x, y
def mod_inverse(n, m):
    return pow(n, -1, m)
def point_addition(res, a, b, m, P):
    if res is None:
        return P
    if P is None:
        return res
    x1, y1 = P
    x2, y2 = res
    if x1 == x2 and y1 == -y2 % m:
        return None
    if x1 != x2:
        slope = ((y2 - y1) * mod_inverse(x2 - x1, m)) % m
    else:
        slope = ((3 * x1 * x1 + a) * mod_inverse(2 * y1, m)) % m
    x3 = (slope * slope - x1 - x2) % m
    y3 = (slope * (x1 - x3) - y1) % m
    return x3, y3
def multiplication(k, a, b, m, P):
    res = None
    temp = P
    for _ in range(k):
        if res is None:
            res = temp
        else:
            res = point_addition(res, a, b, m, temp)
    return res
pub_x, pub_y = generate_point(a, b, m)
public_point = (pub_x, pub_y)
while True:
    k_a = random.randint(2, m - 1)
    k_b = random.randint(2, m - 1)
    pub_point_a = multiplication(k_a, a, b, m, public_point)
    pub_point_b = multiplication(k_b, a, b, m, public_point)
    if pub_point_b is None:
        continue
    shared_key_alice = multiplication(k_a, a, b, m, pub_point_b)
    shared_key_bob = multiplication(k_b, a, b, m, pub_point_a)
    if shared_key_alice is not None and shared_key_bob is not None:
        break
print("Public Point:", public_point)
print("Private Key A:", k_a)
print("Private Key B:", k_b)
print("Public Key A:", pub_point_a)
print("Public Key B:", pub_point_b)
print("Shared Secret (Alice):", shared_key_alice)
print("Shared Secret (Bob):", shared_key_bob)
print("Keys Match:", shared_key_alice == shared_key_bob)
