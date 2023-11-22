from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode
from Crypto.Util.number import bytes_to_long, long_to_bytes

def generate_RSA(bits=1024):
    key = RSA.generate(bits)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    with open("private_key.pem", "wb") as f_priv, open("public_key.pem", "wb") as f_pub:
        f_priv.write(private_key)
        f_pub.write(public_key)

def encrypt_RSA(public_key_file, message_bytes):
    with open(public_key_file, "rb") as f:
        pubkey = RSA.import_key(f.read())
    cipher = PKCS1_OAEP.new(pubkey)
    ciphertext = cipher.encrypt(message_bytes)
    return b64encode(ciphertext).decode('ascii')

def decrypt_RSA(private_key_file, ciphertext_b64):
    with open(private_key_file, "rb") as f:
        privkey = RSA.import_key(f.read())
    cipher = PKCS1_OAEP.new(privkey)
    ciphertext = b64decode(ciphertext_b64)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext

def sign_data(private_key_file, data_bytes):
    with open(private_key_file, "rb") as f:
        privkey = RSA.import_key(f.read())
    h = SHA256.new(data_bytes)
    signer = PKCS1_PSS.new(privkey)
    signature = signer.sign(h)
    return b64encode(signature).decode('ascii')

def verify_sign(public_key_file, signature_b64, data_bytes):
    with open(public_key_file, "rb") as f:
        pubkey = RSA.import_key(f.read())
    h = SHA256.new(data_bytes)
    verifier = PKCS1_PSS.new(pubkey)
    signature = b64decode(signature_b64)
    return verifier.verify(h, signature)

if __name__ == "__main__":
    # 1. Generate RSA keys
    generate_RSA()

    # 2. Read plaintext from mydata.txt
    with open("mydata.txt", "rb") as f:
        data = f.read()

    # 3. Encrypt with public key
    ciphertext_b64 = encrypt_RSA("public_key.pem", data)
    print(f"Encrypted:\n{ciphertext_b64}\n")

    # 4. Decrypt with private key
    decrypted = decrypt_RSA("private_key.pem", ciphertext_b64)
    print(f"Decrypted:\n{decrypted.decode('utf-8')}\n")

    # 5. Sign data with private key
    signature_b64 = sign_data("private_key.pem", data)
    print(f"Signature:\n{signature_b64}\n")

    # 6. Verify signature with public key
    verification = verify_sign("public_key.pem", signature_b64, data)
    print(f"Signature valid? {'Yes' if verification else 'No'}\n")


    chosen_int = 100
    multiplier = 2

    # Encrypt 
    chosen_bytes = chosen_int.to_bytes((chosen_int.bit_length()+7)//8 or 1, 'big')
    multiplier_bytes = multiplier.to_bytes((multiplier.bit_length()+7)//8 or 1, 'big')

    c1_b64 = encrypt_RSA("public_key.pem", chosen_bytes)
    c2_b64 = encrypt_RSA("public_key.pem", multiplier_bytes)

    c1_int = bytes_to_long(b64decode(c1_b64))
    c2_int = bytes_to_long(b64decode(c2_b64))

    with open("public_key.pem", "rb") as f:
        pubkey = RSA.import_key(f.read())

    # Multiply ciphertexts mod n
    modified_int = (c1_int * c2_int) % pubkey.n
    modified_bytes = long_to_bytes(modified_int)

    # Try to decrypt
    with open("private_key.pem", "rb") as f:
        privkey = RSA.import_key(f.read())

    cipher = PKCS1_OAEP.new(privkey)
    try:
        decrypted_modified = cipher.decrypt(modified_bytes)
        print(f"Decrypted:\n{decrypted_modified}\n")
        print("Attack successful")
    except ValueError:
        print("Attack failed\n")
