import hashlib
import string

# Load hashes from hash5.txt
def load_hashes(file_path):
    with open(file_path, 'r') as f:
        return [line.strip().lower() for line in f if line.strip()]

# Save remaining hashes
def save_remaining_hashes(file_path, hashes):
    with open(file_path, 'w') as f:
        for h in hashes:
            f.write(h + '\n')

# Append matched hash to ex2_hash.txt
def append_result(result_file, match_final, match_hash):
    with open(result_file, 'a') as f:
        f.write(f"{match_final}: {match_hash}\n")

def brute_force_match(hashes):
    chars = string.ascii_lowercase + string.digits  # 'abcdefghijklmnopqrstuvwxyz0123456789'

    for c1 in chars:
        for c2 in chars:
            for c3 in chars:
                for c4 in chars:
                    for c5 in chars:
                        c_final = c1 + c2 + c3 + c4 + c5
                        c_hash = hashlib.md5(c_final.encode()).hexdigest()
                        if c_hash in hashes:
                            print(f"Match found!")
                            print(f"string : {c_final}")
                            print(f"Hash : {c_hash}")
                            return c_final, c_hash
    print("No match found.")
    return None, None

# main
hash_file = "hash5.txt"
result_file = "ex2_hash.txt"

while True:
    hashes = load_hashes(hash_file)
    if not hashes:
        print("All hashes matched.")
        break

    match_final, match_hash = brute_force_match(hashes)

    if match_hash is None:
        break

    hashes.remove(match_hash)
    save_remaining_hashes(hash_file, hashes)

    append_result(result_file, match_final, match_hash)