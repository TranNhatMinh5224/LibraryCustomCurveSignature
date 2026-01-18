from .curve import TNM5224
from .field import mod, mod_inv
from .point import Point


def verify(message_hash: int, signature, public_key: Point) -> bool:
    r, s = signature
    n = TNM5224.n

    if not (1 <= r < n and 1 <= s < n):
        return False

    if public_key.is_infinity():
        return False

    if not public_key.is_on_curve():
        return False

    # Subgroup check
    if not public_key.multiply(n).is_infinity():
        return False

    w = mod_inv(s, n)
    u1 = mod(message_hash * w, n)
    u2 = mod(r * w, n)

    G = Point(TNM5224.Gx, TNM5224.Gy)
    X = G.multiply(u1).add(public_key.multiply(u2))

    if X.is_infinity():
        return False

    return mod(X.x, n) == r
