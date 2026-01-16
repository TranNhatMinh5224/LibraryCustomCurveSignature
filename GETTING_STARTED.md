# GETTING STARTED - Hướng dẫn cho người dùng mới

## 📥 Bước 1: Tải mã nguồn

```bash
# Clone repository (hoặc download ZIP)
git clone https://github.com/yourusername/custom-curve-signature.git
cd custom-curve-signature
```

## 🔧 Bước 2: Cài đặt

```bash
# Cài đặt thư viện (editable mode)
pip install -e .

# Hoặc cài đặt từ source
pip install .
```

**Lưu ý:** Thư viện không cần dependencies nào, chỉ cần Python 3.10+

## ✅ Bước 3: Kiểm tra cài đặt

```bash
# Quick test
python quick_test.py

# Full test suite (optional)
python tests/test_comprehensive.py
python tests/test_serialization.py
python tests/test_rfc6979.py
```

## 🚀 Bước 4: Sử dụng trong code

### Tạo file mới `my_test.py`:

```python
from custom_curve_signature import (
    generate_keypair,
    sign,
    verify,
    hash_msg
)

# Generate keys
private_key, public_key = generate_keypair()

# Sign
message = b"Hello World"
msg_hash = hash_msg(message)
signature = sign(msg_hash, private_key)

# Verify
is_valid = verify(msg_hash, signature, public_key)
print(f"Signature valid: {is_valid}")
```

### Chạy:

```bash
python my_test.py
```

## 📚 Ví dụ đầy đủ

Xem file `tests/test_example.py` hoặc đọc [README.md](README.md) để biết thêm chi tiết.

## ❓ Troubleshooting

### Lỗi: ModuleNotFoundError

```bash
# Đảm bảo đã cài đặt:
pip install -e .

# Hoặc chạy từ thư mục gốc với:
python -m pytest tests/
```

### Lỗi: Python version

```bash
# Cần Python 3.10 trở lên
python --version

# Nếu thấp hơn, cài Python mới tại python.org
```

## 🎯 Next Steps

1. ✅ Đọc [README.md](README.md) - Hướng dẫn chi tiết
2. ✅ Xem `tests/test_example.py` - Ví dụ sử dụng
3. ✅ Thử Fabric integration example trong README
4. ✅ Tùy chỉnh cho use case của bạn

---

**Thư viện sẵn sàng sử dụng! 🎉**
