import matplotlib.pyplot as plt
import numpy as np
import math

z = 53684551531801

def pollard(n):
    # Testando várias bases, quando necessário
    bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31] 

    B = int(n**0.20) # limite para k (usaremos k!)

    for base in bases:
        a = base 
        for k in range(2, B + 1):
            a = pow(a, k, n) # a^k (mod n)
            d = math.gcd(a - 1, n)
            
            if 1 < d < n:
                return d, n // d
            
            elif d == n:
                print(f"  -> Falha com base {base} (MDC deu n). Trocando base...")
                break

    return None, None

p, q = pollard(z)

if p == None and q == None:
    print("Falhamos!")

print(f"{z} = {p} x {q}")    
