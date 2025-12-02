import matplotlib.pyplot as plt
import numpy as np
import time
import math

z = 67127581

def pollard(n):
    # Testando várias bases, quando necessário
    bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31] 

    B = int(n**0.50) # limite para k (usaremos k!)
    
    for base in bases:
        a = base 
        for k in range(2, B + 1):
            a = pow(a, k, n) # a^i (mod n)
            d = math.gcd(a - 1, n)
            
            if 1 < d < n:
                return d, n // d
            
            elif d == n:
                print(f"  -> Falha com base {base} (MDC deu n). Trocando base...")
                break

    return None, None

p,q = pollard(z)

if p == None and q == None:
    print("Falhamos!")

print(f"{z} = {p} x {q}")    

# semiprimes = [6, 77, 989, 2291, 97627, 358091, 8846573, 63451711, 553789213, 5276275391, 48965927779, 868082737663, 5163693436199, 53684551531801, 635621477042171, 6750421608780299,68569780649272979]

# def performance(semiprimes, times):
#     for i in range(len(semiprimes)):
#         divs, timer = pollard(semiprimes[i])
#         times.append(timer)
#     return times

# times = []
# times = performance(semiprimes, times)
# times = np.array(times)

# num_digitos = np.array([len(str(n)) for n in semiprimes])

# plt.semilogy(num_digitos, times, 'o-')

# # Plota Gráfico sem escala logaritmica
# # plt.plot(num_digitos, times, 'o-')

# plt.xlabel("Número de Dígitos (k)")
# plt.ylabel("Tempo de Fatoração (s) - Em escala Log")
# plt.title("Tempo vs. Número de Dígitos")
# plt.grid(True)
# plt.show()
