# serialize.py
"""
Serialization utilities for signatures and keys
"""

from typing import Tuple
from .point import Point


def signature_to_bytes(signature: Tuple[int, int]) -> bytes:
    """
    Convert signature (r, s) to fixed-length bytes
    Format: r || s (each 32 bytes, big-endian)
    Total: 64 bytes
    """
    r, s = signature
    
    # Each component is 32 bytes (256 bits)
    r_bytes = r.to_bytes(32, byteorder='big')
    s_bytes = s.to_bytes(32, byteorder='big')
    
    return r_bytes + s_bytes


def signature_from_bytes(sig_bytes: bytes) -> Tuple[int, int]:
    """
    Convert bytes to signature (r, s)
    Expected: 64 bytes
    """
    if len(sig_bytes) != 64:
        raise ValueError(f"Invalid signature length: {len(sig_bytes)} (expected 64)")
    
    r = int.from_bytes(sig_bytes[:32], byteorder='big')
    s = int.from_bytes(sig_bytes[32:64], byteorder='big')
    
    return (r, s)


def signature_to_hex(signature: Tuple[int, int]) -> str:
    """
    Convert signature to hex string
    """
    sig_bytes = signature_to_bytes(signature)
    return sig_bytes.hex()


def signature_from_hex(sig_hex: str) -> Tuple[int, int]:
    """
    Convert hex string to signature
    """
    sig_bytes = bytes.fromhex(sig_hex)
    return signature_from_bytes(sig_bytes)


def private_key_to_bytes(private_key: int) -> bytes:
    """
    Convert private key to bytes (32 bytes)
    """
    return private_key.to_bytes(32, byteorder='big')


def private_key_from_bytes(key_bytes: bytes) -> int:
    """
    Convert bytes to private key
    """
    if len(key_bytes) != 32:
        raise ValueError(f"Invalid private key length: {len(key_bytes)} (expected 32)")
    
    return int.from_bytes(key_bytes, byteorder='big')


def private_key_to_hex(private_key: int) -> str:
    """
    Convert private key to hex string
    """
    return private_key_to_bytes(private_key).hex()


def private_key_from_hex(key_hex: str) -> int:
    """
    Convert hex string to private key
    """
    key_bytes = bytes.fromhex(key_hex)
    return private_key_from_bytes(key_bytes)


def public_key_to_bytes(public_key: Point, compressed: bool = False) -> bytes:
    """
    Convert public key to bytes
    
    Args:
        public_key: Point (x, y)
        compressed: If True, use compressed format (33 bytes)
                   If False, use uncompressed format (65 bytes)
    
    Uncompressed: 0x04 || x || y (65 bytes)
    Compressed: 0x02/0x03 || x (33 bytes)
    """
    if public_key.is_infinity():
        raise ValueError("Cannot serialize point at infinity")
    
    x_bytes = public_key.x.to_bytes(32, byteorder='big')
    
    if compressed:
        # 0x02 if y is even, 0x03 if y is odd
        prefix = 0x02 if public_key.y % 2 == 0 else 0x03
        return bytes([prefix]) + x_bytes
    else:
        # Uncompressed format
        y_bytes = public_key.y.to_bytes(32, byteorder='big')
        return bytes([0x04]) + x_bytes + y_bytes


def public_key_from_bytes(key_bytes: bytes) -> Point:
    """
    Convert bytes to public key
    Supports both compressed (33 bytes) and uncompressed (65 bytes)
    """
    if len(key_bytes) == 65:
        # Uncompressed format
        if key_bytes[0] != 0x04:
            raise ValueError(f"Invalid uncompressed key prefix: {key_bytes[0]:02x}")
        
        x = int.from_bytes(key_bytes[1:33], byteorder='big')
        y = int.from_bytes(key_bytes[33:65], byteorder='big')
        
        point = Point(x, y)
        if not point.is_on_curve():
            raise ValueError("Public key not on curve")
        
        return point
    
    elif len(key_bytes) == 33:
        # Compressed format
        prefix = key_bytes[0]
        if prefix not in (0x02, 0x03):
            raise ValueError(f"Invalid compressed key prefix: {prefix:02x}")
        
        x = int.from_bytes(key_bytes[1:33], byteorder='big')
        
        # Recover y from x
        # y^2 = x^3 + ax + b (mod p)
        from .curve import TNM5224
        from .field import mod
        
        p = TNM5224.p
        a = TNM5224.a
        b = TNM5224.b
        
        y_squared = mod(x**3 + a * x + b, p)
        
        # Compute square root (p ≡ 3 mod 4, so use y = y_squared^((p+1)/4) mod p)
        y = pow(y_squared, (p + 1) // 4, p)
        
        # Verify it's correct
        if mod(y * y, p) != y_squared:
            raise ValueError("Point not on curve (no valid y)")
        
        # Choose correct y based on parity
        if (y % 2 == 0 and prefix == 0x03) or (y % 2 == 1 and prefix == 0x02):
            y = p - y
        
        point = Point(x, y)
        if not point.is_on_curve():
            raise ValueError("Public key not on curve")
        
        return point
    
    else:
        raise ValueError(f"Invalid public key length: {len(key_bytes)}")


def public_key_to_hex(public_key: Point, compressed: bool = False) -> str:
    """
    Convert public key to hex string
    """
    return public_key_to_bytes(public_key, compressed).hex()


def public_key_from_hex(key_hex: str) -> Point:
    """
    Convert hex string to public key
    """
    key_bytes = bytes.fromhex(key_hex)
    return public_key_from_bytes(key_bytes)
