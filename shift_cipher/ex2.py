#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 1
# Simple file read in/out

import argparse
import pathlib

#PNG files always start with this 8-bye header:
PNG_HEADER = b'\x89PNG\r\n\x1a\n'

def encrypt(data: bytes, key: int) -> bytearray:
    return bytearray((b + key) % 256 for b in data)

def decrypt(data: bytes, key: int) -> bytearray:
    return bytearray((b - key) % 256 for b in data)

def brute_force_file(data: bytes, output_path: str):
    for key in range(256):
        candidate = decrypt(data, key)
        if candidate.startswith(PNG_HEADER):
            pathlib.Path(output_path).write_bytes(candidate)
            print(f"Success! PNG found. Key = {key}")
            return
    print(" No valid PNG found with any key.")

def main():
    parser = argparse.ArgumentParser(description="Encrypt/decrypt or brute-force PNG from Caesar byte-shift cipher.")
    parser.add_argument('-i', '--input', required=True, help='Input file path')
    parser.add_argument('-o', '--output', required=True, help='Output file path')
    parser.add_argument('-k', '--key', type=int, choices=range(256), help='Key (0–255)')
    parser.add_argument('-m', '--mode', choices=['e', 'd'], help='Mode: "e" for encrypt, "d" for decrypt')
    args = parser.parse_args()

    # Read input bytes
    data = pathlib.Path(args.input).read_bytes()

    # If key and mode are provided, perform normal encrypt/decrypt
    if args.key is not None and args.mode:
        if args.mode == 'e':
            result = encrypt(data, args.key)
        else:
            result = decrypt(data, args.key)
        pathlib.Path(args.output).write_bytes(result)

    # Otherwise, brute-force mode
    else:
        brute_force_file(data, args.output)

if __name__ == '__main__':
    main()
    