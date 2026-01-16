# sign.py
from .curve import TNM5224
from .field import mod, mod_inv
from .point import Point
from .rfc6979 import generate_k_rfc6979


def sign(message_hash: int, private_key: int, deterministic: bool = True):
    """
    Ký ECDSA với RFC 6979 (deterministic nonce)
    
    Args:
      - message_hash: int (đã hash)
      - private_key: d (private key)
      - deterministic: Nếu True, dùng RFC 6979 (khuyên dùng)
                      Nếu False, dùng random k (không an toàn)
    
    Returns:
      - (r, s): ECDSA signature
    
    Note: RFC 6979 prevents nonce reuse attacks by generating 
          deterministic k from (private_key, message_hash).
          Cùng message + key → cùng signature (reproducible & secure)
    """

    n = TNM5224.n
    G = Point(TNM5224.Gx, TNM5224.Gy)

    if deterministic:
        # RFC 6979: Deterministic k generation
        k = generate_k_rfc6979(n, private_key, message_hash)
        
        # Tính kG
        R = G.multiply(k)
        r = mod(R.x, n)
        
        # Với RFC 6979, r không bao giờ = 0 (đã đảm bảo trong thuật toán)
        # Nhưng vẫn kiểm tra cho an toàn
        if r == 0:
            raise ValueError("RFC 6979 generated invalid r=0 (should not happen)")
        
        # s = k^-1 (e + d*r) mod n
        k_inv = mod_inv(k, n)
        s = mod(k_inv * (message_hash + private_key * r), n)
        
        if s == 0:
            raise ValueError("Generated invalid s=0 (should not happen)")
        
        return (r, s)
    
    else:
        # Legacy: Random k (NOT RECOMMENDED - kept for compatibility)
        import secrets
        import warnings
        
        warnings.warn(
            "Using random k is NOT recommended. "
            "Use deterministic=True (RFC 6979) to prevent nonce reuse attacks.",
            category=UserWarning,
            stacklevel=2
        )
        
        while True:
            # Sinh k ngẫu nhiên trong [1, n-1]
            k = secrets.randbelow(n - 1) + 1

            # Tính kG
            R = G.multiply(k)
            r = mod(R.x, n)

            if r == 0:
                continue

            # s = k^-1 (e + d*r) mod n
            k_inv = mod_inv(k, n)
            s = mod(k_inv * (message_hash + private_key * r), n)

            if s == 0:
                continue

            return (r, s)
