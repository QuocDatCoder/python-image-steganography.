from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

class AESCrypt:
    # Key must be 16, 24, or 32 bytes long. Java used "1Hbfh667adfDEJ78" (16 bytes)
    KEY = b'1Hbfh667adfDEJ78'
    
    @staticmethod
    def encrypt(plaintext: str) -> str:
        """Encrypts plaintext using AES-ECB (to match Java default) and returns base64 string."""
        if not plaintext:
            return ""
        cipher = AES.new(AESCrypt.KEY, AES.MODE_ECB)
        padded_data = pad(plaintext.encode('utf-8'), AES.block_size)
        encrypted_bytes = cipher.encrypt(padded_data)
        return base64.b64encode(encrypted_bytes).decode('utf-8')

    @staticmethod
    def decrypt(ciphertext_b64: str) -> str:
        """Decrypts base64 encoded ciphertext using AES-ECB."""
        if not ciphertext_b64:
            return ""
        try:
            cipher = AES.new(AESCrypt.KEY, AES.MODE_ECB)
            encrypted_bytes = base64.b64decode(ciphertext_b64)
            decrypted_padded = cipher.decrypt(encrypted_bytes)
            return unpad(decrypted_padded, AES.block_size).decode('utf-8')
        except Exception as e:
            print(f"Decryption error: {e}")
            return None
