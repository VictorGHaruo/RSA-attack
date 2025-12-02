import time

def extended_gcd(a, b):
    x0, y0 = 1, 0
    x1, y1 = 0, 1

    while b != 0:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1

    return a, x0, y0   # gcd, x, y

# Números teste, mesmo n relativamente grande
n = 112497897258763
e1 = 17
e2 = 65537
m = 123456789

c1 = pow(m, e1, n)
c2 = pow(m, e2, n)
print("c1 =", c1)
print("c2 =", c2)


start = time.time()
g, a, b = extended_gcd(e1, e2)
# pow() lida com expoentes negativos automaticamente
m_rec = (pow(c1, a, n) * pow(c2, b, n)) % n

end = time.time()

print("a =", a, " b =", b)
print("M descoberto =", m_rec)
print(f"Em {end - start} segundos.")