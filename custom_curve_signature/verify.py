# verify.py
from .curve import TNM5224
from .field import mod, mod_inv
from .point import Point


def verify(message_hash: int, signature, public_key: Point) -> bool:
    """
    Verify chữ ký ECDSA
    """

    r, s = signature
    n = TNM5224.n

    # Check range
    if not (1 <= r < n and 1 <= s < n):
        return False

    w = mod_inv(s, n)
    u1 = mod(message_hash * w, n)
    u2 = mod(r * w, n)

    G = Point(TNM5224.Gx, TNM5224.Gy)

    # X = u1*G + u2*Q
    X = G.multiply(u1).add(public_key.multiply(u2))

    if X.is_infinity():
        return False

    return mod(X.x, n) == r
