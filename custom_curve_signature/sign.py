from .curve import TNM5224
from .field import mod, mod_inv
from .point import Point
from .rfc6979 import generate_k_rfc6979


def sign(message_hash: int, private_key: int, deterministic: bool = True):
    n = TNM5224.n
    G = Point(TNM5224.Gx, TNM5224.Gy)

    if not (1 <= private_key < n):
        raise ValueError("Invalid private key")

    if deterministic:
        k = generate_k_rfc6979(n, private_key, message_hash)
    else:
        import secrets
        k = secrets.randbelow(n - 1) + 1

    R = G.multiply(k)
    r = mod(R.x, n)
    if r == 0:
        raise ValueError("Invalid r")

    k_inv = mod_inv(k, n)
    s = mod(k_inv * (message_hash + private_key * r), n)
    if s == 0:
        raise ValueError("Invalid s")

    # Low-S normalization
    if s > n // 2:
        s = n - s

    return (r, s)
