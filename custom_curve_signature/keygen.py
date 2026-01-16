# keygen.py
import secrets
from .curve import TNM5224
from .point import Point


def random_int(max_n: int) -> int:
    """
    Sinh số nguyên ngẫu nhiên trong [1, max_n - 1]
    (tương đương randomBN trong JS)
    """
    while True:
        r = secrets.randbelow(max_n)
        if 1 <= r < max_n:
            return r


def generate_keypair():
    """
    Sinh cặp khóa ECDSA:
    - private key d
    - public key Q = d * G
    """
    d = random_int(TNM5224.n)   # private key
    G = Point(TNM5224.Gx, TNM5224.Gy)
    Q = G.multiply(d)           # public key

    return d, Q
