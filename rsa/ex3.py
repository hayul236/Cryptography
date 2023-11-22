from Crypto.PublicKey import RSA
import rsa
import base64

def int_to_bytes(i, key):
    length = (key.n.bit_length() + 7) // 8
    return i.to_bytes(length, byteorder='big')

def int_to_b64(i, key):
    return base64.b64encode(int_to_bytes(i, key)).decode('ascii')

def pretty_print_b64(s, width=64):
    return '\n'.join(s[i:i+width] for i in range(0, len(s), width))

if __name__ == "__main__":
    with open("mykey.pem.pub", "r") as pubkey_file:
        pubkey = RSA.import_key(pubkey_file.read())
    with open("mykey.pem.priv", "r") as privkey_file:
        privkey = RSA.import_key(privkey_file.read())

    chosen_int = 100
    s = 2
    print(f"Encrypting: {chosen_int}\n")

    y = rsa.encrypt(chosen_int, pubkey.e, pubkey.n)
    print("Result:")
    print(pretty_print_b64(int_to_b64(y, pubkey)), "\n")

    y_s = rsa.encrypt(s, pubkey.e, pubkey.n)
    m = (y * y_s) % pubkey.n
    print("Modified to:")
    print(pretty_print_b64(int_to_b64(m, pubkey)), "\n")

    decrypted = rsa.decrypt(m, privkey.d, privkey.n)
    print(f"Decrypted: {decrypted}\n")

    assert chosen_int * s == decrypted