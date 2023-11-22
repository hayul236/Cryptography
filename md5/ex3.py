import hashlib
import string
import random

# Load recovered passwords from ex2_hash.txt
def load_recovered_passwords(file_path):
    passwords = []
    with open(file_path, 'r') as f:
        for line in f:
            if ':' in line:
                parts = line.strip().split(':')
                pwd = parts[0].strip()
                passwords.append(pwd)
    return passwords

# Generate salted hashes
def generate_salted_hashes(passwords):
    salted_info = []
    for pwd in passwords:
        salt = random.choice(string.ascii_lowercase)
        salted_pwd = pwd + salt
        salted_hash = hashlib.md5(salted_pwd.encode()).hexdigest()
        salted_info.append((salted_pwd, salted_hash, salt))
    return salted_info

# Save salted hash results
def write_salted_outputs(salted_info, hash_file, plain_file):
    with open(hash_file, 'w') as f_hashes, open(plain_file, 'w') as f_plain:
        for salted_pwd, salted_hash, salt in salted_info:
            f_hashes.write(f"{salted_hash} {salt}\n")
            f_plain.write(f"{salted_pwd}\n")

# main (generate salted hash)
ex2_input = "ex2_hash.txt"
salted_output = "salted6.txt"
plain_output = "plain6.txt"

recovered_pwds = load_recovered_passwords(ex2_input)
salted_data = generate_salted_hashes(recovered_pwds)
write_salted_outputs(salted_data, salted_output, plain_output)

print(f"Salted hashes written to '{salted_output}'")
print(f"Plain salted strings written to '{plain_output}'")

def load_hashes(file_path):
    with open(file_path, 'r') as f:
        return [(line.strip().split()[0].lower(), line.strip().split()[1]) for line in f if line.strip()]
    
def brute_force_match(target_hash, salt):
    chars = string.ascii_lowercase + string.digits  # 'abcdefghijklmnopqrstuvwxyz0123456789'

    for c1 in chars:
        for c2 in chars:
            for c3 in chars:
                for c4 in chars:
                    for c5 in chars:
                        c_final = c1 + c2 + c3 + c4 + c5
                        chash_final = c_final + salt
                        hashed = hashlib.md5(chash_final.encode()).hexdigest()
                        if hashed == target_hash:
                            print("Match found!")
                            print(f"String : {c_final}")
                            print(f"Salt   : {salt}")
                            print(f"Hash   : {hashed}")
                            return c_final, hashed
    print(f"No match found for hash: {target_hash} with salt: {salt}")
    return None, None

# main
hash_file = "salted6.txt"

hashes = load_hashes(hash_file)

for target_hash, salt in hashes:
    match_final, match_hash = brute_force_match(target_hash, salt)

    
    if match_hash is not None:
        print(f"{match_final + salt} -> {match_hash}\n")