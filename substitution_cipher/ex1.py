def load_cipher(filename):
    with open(filename, 'r') as f:
        return f.read()

def apply_substitution_replace(text, sub_map):
    for cipher_char, plain_char in sub_map.items():
        text = text.replace(cipher_char, plain_char)
    return text

def main():
    substitution_map = {
        'A': 'k', 'B': 'l', 'C': 'm', 'D': 'n', 'E': 'o', 'F': 'p', 'G': 'q', 'H': 'r', 'I': 's', 'J': 't',
        'K': 'u', 'L': 'v', 'M': 'w', 'N': 'x', 'O': 'y', 'P': 'z', 'Q': 'a', 'R': 'b', 'S': 'c', 'T': 'd',
        'U': 'e', 'V': 'f', 'W': 'g', 'X': 'h', 'Y': 'i', 'Z': 'j'
    }

    ciphertext = load_cipher("story_cipher.txt")
    decrypted_text = apply_substitution_replace(ciphertext, substitution_map)

    with open("solution.txt", "w") as f_out:
        f_out.write(decrypted_text)

    print("Decryption complete. Output saved to solution.txt")

if __name__ == "__main__":
    main()