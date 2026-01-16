# __init__.py
"""
Custom Curve Signature Library
Digital signature using TNM5224 elliptic curve with RFC 6979 deterministic signatures
"""

from .curve import TNM5224
from .keygen import generate_keypair
from .sign import sign
from .verify import verify
from .hash import hash_msg, hash_with_domain
from .point import Point
from .rfc6979 import generate_k_rfc6979
from .serialize import (
    signature_to_bytes,
    signature_from_bytes,
    signature_to_hex,
    signature_from_hex,
    private_key_to_bytes,
    private_key_from_bytes,
    private_key_to_hex,
    private_key_from_hex,
    public_key_to_bytes,
    public_key_from_bytes,
    public_key_to_hex,
    public_key_from_hex,
)

__version__ = "0.2.0"

__all__ = [
    # Version
    "__version__",
    # Core
    "TNM5224",
    "Point",
    "generate_keypair",
    "sign",
    "verify",
    # Hash
    "hash_msg",
    "hash_with_domain",
    # Serialization
    "signature_to_bytes",
    "signature_from_bytes",
    "signature_to_hex",
    "signature_from_hex",
    "private_key_to_bytes",
    "private_key_from_bytes",
    "private_key_to_hex",
    "private_key_from_hex",
    "public_key_to_bytes",
    "public_key_from_bytes",
    "public_key_to_hex",
    "public_key_from_hex",
]
