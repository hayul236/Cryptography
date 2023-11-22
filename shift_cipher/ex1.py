#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 1
# Simple file read in/out

import argparse
import string

#100 printable chars
ALPHABET = string.printable
N = len(ALPHABET)

def shift_char(c, key, mode):
    if c in ALPHABET:
        idx = ALPHABET.index(c)
        #encryption
        if mode == 'e':  
            new_idx = (idx + key) % N
        #decryption
        elif mode == 'd':
            new_idx = (idx - key) % N
        return ALPHABET[new_idx]
    else:
        return c  # Leave non-printable alone

def process_text(data, key, mode):
    return ''.join(shift_char(c, key, mode) for c in data)

def main():
    # CLI setup
    parser = argparse.ArgumentParser(description="Encrypt or decrypt a file using a Caesar-like cipher.")
    parser.add_argument("-i", "--input", required=True, help="Input file path")
    parser.add_argument("-o", "--output", required=True, help="Output file path")
    parser.add_argument("-k", "--key", type=int, required=True, help="Encryption/Decryption key (integer)")
    parser.add_argument("-m", "--mode", choices=['e', 'd'], required=True, help="Mode: 'e' for encrypt, 'd' for decrypt")
    args = parser.parse_args()

    with open(args.input, 'r', encoding='utf-8') as in_file:
        data = in_file.read()

    result = process_text(data, args.key, args.mode)
    
    with open(args.output, 'w', encoding='utf-8') as out_file:
        out_file.write(result)


if __name__ == '__main__':
    main()