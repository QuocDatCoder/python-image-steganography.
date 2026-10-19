from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

class AESCrypt:
    @staticmethod
    def _get_valid_key(key: str) -> bytes:
        """Chuẩn hóa khóa người dùng nhập thành đúng 16 byte (chuẩn AES-128)."""
        if not key:
            key = "1Hbfh667adfDEJ78" # Khóa mặc định nếu để trống
        
        key_bytes = key.encode('utf-8')
        # Đảm bảo độ dài khóa đủ 16 byte (cắt bớt nếu thừa, thêm ký tự '0' nếu thiếu)
        if len(key_bytes) < 16:
            key_bytes = key_bytes.ljust(16, b'0')
        elif len(key_bytes) > 16:
            key_bytes = key_bytes[:16]
        return key_bytes

    @staticmethod
    def encrypt(plaintext: str, key: str) -> str:
        """Mã hóa văn bản sử dụng khóa động (Dynamic Key) với AES-ECB."""
        if not plaintext:
            return ""
        valid_key = AESCrypt._get_valid_key(key)
        cipher = AES.new(valid_key, AES.MODE_ECB)
        padded_data = pad(plaintext.encode('utf-8'), AES.block_size)
        encrypted_bytes = cipher.encrypt(padded_data)
        return base64.b64encode(encrypted_bytes).decode('utf-8')

    @staticmethod
    def decrypt(ciphertext_b64: str, key: str) -> str:
        """Giải mã chuỗi base64 sử dụng khóa động (Dynamic Key) với AES-ECB."""
        if not ciphertext_b64:
            return ""
        try:
            valid_key = AESCrypt._get_valid_key(key)
            cipher = AES.new(valid_key, AES.MODE_ECB)
            encrypted_bytes = base64.b64decode(ciphertext_b64)
            decrypted_padded = cipher.decrypt(encrypted_bytes)
            return unpad(decrypted_padded, AES.block_size).decode('utf-8')
        except Exception as e:
            print(f"Decryption error (Khóa không đúng hoặc dữ liệu hỏng): {e}")
            return None