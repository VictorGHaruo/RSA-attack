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

def restoChines(crips, mods):
    N = 1
    for n in mods:
        N *= n
    x = 0
    for c, n in zip(crips, mods):
        Mi = N // n
        _, inv, _ = extended_gcd(Mi, n)
        inv %= n
        x += c * inv * Mi

    return x % N

n1 = 112497897258763
n2 = 6750421608780299
n3 = 5163693436199
e = 3
m = 123456789

c1 = pow(m, e, n1)
c2 = pow(m, e, n2)
c3 = pow(m, e, n3)

print("Usando e = 3 para todos!")
print("Mensagem verdadeira = ", m)
print("c1 = ", c1)
print("c2 = ", c2)
print("c3 = ", c3)
print()

start = time.time()

# print(m**3 < n1*n2*n3)
C = restoChines([c1, c2, c3], [n1, n2, n3])
# print(C < n1*n2*n3)
end = time.time()
print("C' encontrado = ", C)
print("C é menor que N1N2N3? ", C < n1*n2*n3)
print("M encontrada = ", round(C**(1/3)))
print(f"Em {end - start} segundos.")