#!/usr/bin/env python3
# ECB wrapper skeleton file for 50.042 FCS

from present import *
import argparse

nokeybits = 80
blocksize = 64

def ecb(infile, outfile, key, mode):
    # Read input file as bytes
    with open(infile, "rb") as f:
        data = f.read()

    if len(data) % 8 != 0:
        padding_len = 8 - (len(data) % 8)
        data += b'\x00' * padding_len

    output = bytearray()

    for i in range(0, len(data), 8):
        block_bytes = data[i:i+8]
        block_int = int.from_bytes(block_bytes, byteorder='big')

        if mode == 'encrypt':
            processed_int = present(block_int, key)
        elif mode == 'decrypt':
            processed_int = present_inv(block_int, key)
        else:
            raise ValueError("Invalid mode, must be 'encrypt' or 'decrypt'")

        output.extend(processed_int.to_bytes(8, byteorder='big'))

    # Write output bytes to output file
    with open(outfile, "wb") as f:
        f.write(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Block cipher using ECB mode.')
    parser.add_argument('-i', dest='infile', required=True, help='input file')
    parser.add_argument('-o', dest='outfile', required=True, help='output file')
    parser.add_argument('-k', dest='keyfile', required=True, help='key file')
    parser.add_argument('-m', dest='mode', required=True, choices=['encrypt', 'decrypt'], help='mode')

    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile
    keyfile = args.keyfile
    mode = args.mode

    with open(keyfile, 'r') as f:
        key_hex = f.read().strip()
    key = int(key_hex, 16)

    ecb(infile, outfile, key, mode)
