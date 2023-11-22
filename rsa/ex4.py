from Crypto.PublicKey import RSA
import rsa
import secrets

if __name__ == "__main__":
    with open("mykey.pem.pub", "r") as pubkey_file:
        pubkey = RSA.import_key(pubkey_file.read())
    with open("mykey.pem.priv", "r") as privkey_file:
        privkey = RSA.import_key(privkey_file.read())

    s = secrets.SystemRandom().randint(0, 2**1024)

    x = rsa.encrypt(s, pubkey.e, pubkey.n)
    
    x_prime = rsa.encrypt(s, pubkey.e, pubkey.n)

    print(f"s: {s}\n")
    print(f"x: {x}\n")
    print(f"x': {x_prime}\n")

    if x == x_prime:
        print("accepted")
    else:
        print("rejected")