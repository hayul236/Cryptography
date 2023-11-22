# 50.042 FCS Lab 5 Modular Arithmetic
# Year 2025

import copy
class Polynomial2:
    def __init__(self, coeffs):
        self.coeffs = [c % 2 for c in coeffs]
        while len(self.coeffs) > 1 and self.coeffs[-1] == 0:
            self.coeffs.pop()

    def add(self, p2):
        maxlen = max(len(self.coeffs), len(p2.coeffs))
        result = []
        for i in range(maxlen):
            a = self.coeffs[i] if i < len(self.coeffs) else 0
            b = p2.coeffs[i] if i < len(p2.coeffs) else 0
            result.append(a ^ b)
        return Polynomial2(result)

    def sub(self, p2):
        return self.add(p2)

    def mul(self, p2, modp=None):
        a = self.coeffs
        b = p2.coeffs
        result = [0] * (len(a) + len(b) - 1)
        for i in range(len(a)):
            if a[i]:
                for j in range(len(b)):
                    result[i + j] ^= b[j]
        product = Polynomial2(result)
        if modp:
            _, remainder = product.div(modp)
            return remainder
        return product

    def div(self, p2):
        a = self.coeffs[:]
        b = p2.coeffs[:]
        if not any(b):
            raise ZeroDivisionError("Cannot divide by zero polynomial")

        q = [0] * (len(a) - len(b) + 1) if len(a) >= len(b) else [0]
        r = a[:]

        d = len(b) - 1
        c = b[-1] 

        while len(r) >= len(b):
            deg_r = len(r) - 1
            lc_r = r[-1]
            if lc_r == 1:
                shift = deg_r - d
                q[shift] = 1

                # s * b
                sb = [0] * (shift + len(b))
                for i in range(len(b)):
                    sb[i + shift] = b[i]

                # r = r - sb
                r = [(r[i] if i < len(r) else 0) ^ (sb[i] if i < len(sb) else 0)
                     for i in range(max(len(r), len(sb)))]
            r.pop()
        return Polynomial2(q), Polynomial2(r)

    def __str__(self):
        terms = []
        for i, c in enumerate(self.coeffs):
            if c:
                if i == 0:
                    terms.append("1")
                elif i == 1:
                    terms.append("x")
                else:
                    terms.append(f"x^{i}")
        return " + ".join(reversed(terms)) if terms else "0"

    def getInt(p):
        val = 0
        for i, bit in enumerate(p.coeffs):
            if bit:
                val |= (1 << i)
        return val

class GF2N:
    affinemat=[[1,0,0,0,1,1,1,1],
               [1,1,0,0,0,1,1,1],
               [1,1,1,0,0,0,1,1],
               [1,1,1,1,0,0,0,1],
               [1,1,1,1,1,0,0,0],
               [0,1,1,1,1,1,0,0],
               [0,0,1,1,1,1,1,0],
               [0,0,0,1,1,1,1,1]]

    def __init__(self, x, n=8, ip=Polynomial2([1,1,0,1,1,0,0,0,1])):
        self.n = n
        self.ip = ip
        coeffs = [(x >> i) & 1 for i in range(n)]
        self.p = Polynomial2(coeffs)

    def add(self, g2):
        result_poly = self.p.add(g2.p)
        return GF2N(Polynomial2.getInt(result_poly), self.n, self.ip)

    def sub(self, g2):
        result_poly = self.p.sub(g2.p)
        return GF2N(Polynomial2.getInt(result_poly), self.n, self.ip)

    def mul(self, g2):
        result_poly = self.p.mul(g2.p, self.ip)
        return GF2N(Polynomial2.getInt(result_poly), self.n, self.ip)

    def div(self, g2):
        q, r = self.p.div(g2.p)
        gq = GF2N(Polynomial2.getInt(q), self.n, self.ip)
        gr = GF2N(Polynomial2.getInt(r), self.n, self.ip)
        return gq, gr

    def getPolynomial2(self):
        return self.p

    def __str__(self):
        return str(self.getInt())

    def getInt(self):
        return Polynomial2.getInt(self.p)

    def mulInv(self):
        pass

    def affineMap(self):
        pass

def main():
    print('\nTest 1')
    print('======')
    print('p1 = x^5 + x^2 + x')
    print('p2 = x^3 + x^2 + 1')
    p1 = Polynomial2([0,1,1,0,0,1])
    p2 = Polynomial2([1,0,1,1])
    p3 = p1.add(p2)
    print('p3 = p1 + p2 =', p3)

    print('\nTest 2')
    print('======')
    print('p4 = x^7 + x^4 + x^3 + x^2 + x')
    print('modp = x^8 + x^7 + x^5 + x^4 + 1')
    p4 = Polynomial2([0,1,1,1,1,0,0,1])
    modp = Polynomial2([1,0,0,0,1,1,0,1,1])
    p5 = p1.mul(p4, modp)
    print('p5 = p1 * p4 mod (modp) =', p5)

    print('\nTest 3')
    print('======')
    print('p6 = x^12 + x^7 + x^2')
    print('p7 = x^8 + x^4 + x^3 + x + 1')
    p6 = Polynomial2([0,0,1,0,0,0,0,1,0,0,0,0,1])    
    p7 = Polynomial2([1,1,0,1,1,0,0,0,1])
    p8q, p8r = p6.div(p7)
    print('q for p6 / p7 =', p8q)
    print('r for p6 / p7 =', p8r)

    print('\nTest 4')
    print('======')
    g1 = GF2N(100)
    g2 = GF2N(5)
    print('g1 =', g1.getPolynomial2())
    print('g2 =', g2.getPolynomial2())
    g3 = g1.add(g2)
    print('g1 + g2 =', g3)

    print('\nTest 5')
    print('======')
    ip = Polynomial2([1,1,0,0,1])
    print('irreducible polynomial', ip)
    g4 = GF2N(0b1101, 4, ip)
    g5 = GF2N(0b110, 4, ip)
    print('g4 =', g4.getPolynomial2())
    print('g5 =', g5.getPolynomial2())
    g6 = g4.mul(g5)
    print('g4 * g5 =', g6.p)

    print('\nTest 6')
    print('======')
    g7 = GF2N(0b1000010000100, 13, None)
    g8 = GF2N(0b100011011, 13, None)
    print('g7 =', g7.getPolynomial2())
    print('g8 =', g8.getPolynomial2())
    q, r = g7.div(g8)
    print('g7 / g8 =')
    print('q =', q.getPolynomial2())
    print('r =', r.getPolynomial2())

    print('\nTest 7')
    print('======')
    ip = Polynomial2([1,1,0,0,1])
    print('irreducible polynomial', ip)
    g9 = GF2N(0b101, 4, ip)
    print('g9 =', g9.getPolynomial2())
    print('inverse of g9 =', g9.mulInv().getPolynomial2())

    print('\nTest 8')
    print('======')
    ip = Polynomial2([1,1,0,1,1,0,0,0,1])
    print('irreducible polynomial', ip)
    g10 = GF2N(0xc2, 8, ip)
    print('g10 = 0xc2')
    g11 = g10.mulInv()
    print('inverse of g10 = g11 =', hex(g11.getInt()))
    g12 = g11.affineMap()
    print('affine map of g11 =', hex(g12.getInt()))

if __name__ == "__main__":
    main()
