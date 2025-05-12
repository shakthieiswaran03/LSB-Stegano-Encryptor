from steganography import encode_image, decode_image
from crypto_utils import encrypt_text, decrypt_text

def main():
    choice = input("1. Encode\n2. Decode\nSelect: ")
    
    if choice == '1':
        image_path = input("Enter image path to hide text: ").strip()
        out_path = input("Enter output image path (.png recommended): ").strip()
        message = input("Enter message to hide: ").strip()
        password = input("Enter password: ").strip()

        encrypted_message = encrypt_text(message, password)
        encode_image(image_path, out_path, encrypted_message)

        return 

    elif choice == '2':
        image_path = input("Enter stego image path: ").strip()
        password = input("Enter password: ").strip()

        encrypted = decode_image(image_path)
        if not encrypted:
            print("No data found in image.")
            return

        print("\n[DEBUG] Extracted Encrypted Text:\n", encrypted)

        decrypted = decrypt_text(encrypted, password)
        if decrypted:
            print("Hidden Message:", decrypted)
        else:
            print("Failed to decrypt. Wrong password or corrupted data.")

        return

    else:
        print("Invalid choice.")
        return

if __name__ == '__main__':
    main()
