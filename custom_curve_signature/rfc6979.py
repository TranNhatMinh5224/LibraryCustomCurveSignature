# rfc6979.py
"""
RFC 6979: Deterministic Usage of the Digital Signature Algorithm (DSA) and 
Elliptic Curve Digital Signature Algorithm (ECDSA)

Generates deterministic k values for ECDSA to prevent nonce reuse attacks.
"""

import hmac
import hashlib
from typing import Tuple


def bits_to_int(b: bytes, qlen: int) -> int:
    """
    Convert bytes to integer, taking only qlen bits
    """
    z = int.from_bytes(b, byteorder='big')
    # If longer than qlen, take leftmost qlen bits
    blen = len(b) * 8
    if blen > qlen:
        z >>= (blen - qlen)
    return z


def int_to_bytes(x: int, rlen: int) -> bytes:
    """
    Convert integer to bytes with fixed length rlen
    """
    return x.to_bytes(rlen, byteorder='big')


def generate_k_rfc6979(
    n: int,
    private_key: int,
    message_hash: int,
    hash_func=hashlib.sha256
) -> int:
    """
    Generate deterministic k for ECDSA signature according to RFC 6979
    
    Args:
        n: Curve order
        private_key: Private key (d)
        message_hash: Hash of the message (already hashed)
        hash_func: Hash function to use (default: SHA-256)
    
    Returns:
        Deterministic k value in range [1, n-1]
    
    Reference: https://tools.ietf.org/html/rfc6979
    """
    
    # Step a: Process message hash
    h1 = message_hash
    
    # Hash output length in bytes
    hlen = hash_func().digest_size
    
    # Curve order length in bits
    qlen = n.bit_length()
    
    # Curve order length in bytes (rounded up)
    rlen = (qlen + 7) // 8
    
    # Step b: h1 as bytes
    h1_bytes = int_to_bytes(h1, rlen)
    
    # Step c: private key as bytes
    x_bytes = int_to_bytes(private_key, rlen)
    
    # Step d: V = 0x01 0x01 0x01 ... (hlen bytes)
    V = b'\x01' * hlen
    
    # Step e: K = 0x00 0x00 0x00 ... (hlen bytes)
    K = b'\x00' * hlen
    
    # Step f: K = HMAC_K(V || 0x00 || x || h1)
    K = hmac.new(K, V + b'\x00' + x_bytes + h1_bytes, hash_func).digest()
    
    # Step g: V = HMAC_K(V)
    V = hmac.new(K, V, hash_func).digest()
    
    # Step h: K = HMAC_K(V || 0x01 || x || h1)
    K = hmac.new(K, V + b'\x01' + x_bytes + h1_bytes, hash_func).digest()
    
    # Step i: V = HMAC_K(V)
    V = hmac.new(K, V, hash_func).digest()
    
    # Step h: Generate k
    while True:
        # Step h.1: Set T to empty
        T = b''
        
        # Step h.2: While len(T) < rlen
        while len(T) < rlen:
            V = hmac.new(K, V, hash_func).digest()
            T = T + V
        
        # Step h.3: Compute k
        k = bits_to_int(T, qlen)
        
        # If k is in [1, n-1], return it
        if 1 <= k < n:
            return k
        
        # Otherwise, update K and V and try again
        K = hmac.new(K, V + b'\x00', hash_func).digest()
        V = hmac.new(K, V, hash_func).digest()
