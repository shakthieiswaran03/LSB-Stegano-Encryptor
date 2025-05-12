from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib

def get_key(password):
    return hashlib.sha256(password.encode()).digest()

def encrypt_text(text, password):
    key = get_key(password)
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(text.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv + ":" + ct

def decrypt_text(encrypted_text, password):
    key = get_key(password)

    try:
        iv, ct = encrypted_text.split(":")
    except Exception as e:
        print(" Error: Unable to split encrypted text.")
        print(f"[Error Info] {str(e)}")
        return None

    print(f"[DEBUG] IV: {iv}")
    print(f"[DEBUG] Ciphertext: {ct}")

    try:
        iv = base64.b64decode(iv)
        ct = base64.b64decode(ct.split("ÿ")[0])
    except Exception as e:
        print(" Error: Base64 decoding failed.")
        print(f"[Error Info] {str(e)}")
        return None

    print(f"[DEBUG] Decoded IV: {iv}")
    print(f"[DEBUG] Decoded Ciphertext: {ct}")

    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode('utf-8')
    except Exception as e:
        print(" Error: Decryption failed.")
        print(f"[Error Info] {str(e)}")
        return None
