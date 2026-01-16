# hash.py
import hashlib


def hash_msg(data: bytes) -> int:
    """
    Hash message bằng SHA-256
    Trả về số nguyên (big-endian)
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes")

    digest = hashlib.sha256(data).digest()
    return int.from_bytes(digest, byteorder="big")


def hash_with_domain(data: bytes, domain: str = "TNM5224", context: str = "GENERAL", version: str = "v1") -> int:
    """
    Hash message với domain separation để tránh signature reuse
    
    Args:
        data: Message cần hash
        domain: Tên curve/protocol (default: "TNM5224")
        context: Context/use-case (ví dụ: "DEGREE", "CERTIFICATE", "TRANSACTION")
        version: Version của format (default: "v1")
    
    Returns:
        Hash value as integer
    
    Example:
        hash_with_domain(cert_data, context="DEGREE")
        -> Hash("TNM5224::DEGREE::v1" || cert_data)
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes")
    
    # Tạo domain separator
    separator = f"{domain}::{context}::{version}".encode('utf-8')
    
    # Hash với domain separation
    full_data = separator + b"::" + data
    digest = hashlib.sha256(full_data).digest()
    
    return int.from_bytes(digest, byteorder="big")
