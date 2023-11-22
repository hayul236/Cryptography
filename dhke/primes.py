# 50.042 FCS Lab 6 template
# Year 2025

import random
def square_multiply(a, x, n):
    y = 1
    n_b = x.bit_length()  #n_b as number of bits in x
    for i in reversed(range(n_b)):
        y = (y * y) % n  # square
        if (x >> i) & 1:  # check if the ith bit is 1
            y = (y * a) % n  # multiply
    return y

def miller_rabin(n, a):
    if n <= 3:
        return n == 2 or n == 3
    if n % 2 == 0:
        return False

    # n-1 as 2^s * d
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    # a^d mod n
    x = square_multiply(a, d, n)

    if x == 1 or x == n - 1:
        return True

    # repeat squaring   
    for _ in range(s - 1):
        x = (x * x) % n
        if x == n - 1:
            return True
        if x == 1:
            return False

    return False

def gen_prime_nbits(n):
    while True:
        candidate = random.getrandbits(n)
        candidate |= (1 << (n - 1)) | 1  # Ensure it's odd and n bits

        for a in [2, 3, 5, 7, 11]:
            if not miller_rabin(candidate, a):
                break  # Failed
        else:
            return candidate  
        
if __name__=="__main__":
    print('Is 561 a prime?')
    print(miller_rabin(561,2))
    print('Is 27 a prime?')
    print(miller_rabin(27,2))
    print('Is 61 a prime?')
    print(miller_rabin(61,2))

    print('Random number (100 bits):')
    print(gen_prime_nbits(100))
    print('Random number (80 bits):')
    print(gen_prime_nbits(80))
