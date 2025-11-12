import matplotlib.pyplot as plt
import numpy as np
import time
def naive(n):
    begin = time.time()
    div = []
    while (n%2 == 0):
        div.append(2)
        n = n//2
    i = 3
    while i*i <= n:
        print(i)            
        while n%i == 0:
            div.append(i)
            n = n//i
        i = i + 2

    end = time.time()
    if n > 1:
        div.append(n)
    return div, end-begin

def performance(semiprimes, times):
    for i in range(len(semiprimes)):
        divs, timer = naive(semiprimes[i])
        times.append(timer)
    return times

semiprimes = [6, 77, 989, 2291, 97627, 358091, 8846573, 63451711, 553789213, 5276275391, 48965927779, 868082737663, 5163693436199, 53684551531801, 635621477042171, 6750421608780299,68569780649272979]

times = []
times = performance(semiprimes, times)
times = np.array(times)

num_digitos = np.array([len(str(n)) for n in semiprimes])

plt.semilogy(num_digitos, times, 'o-')

# Plota Gráfico sem escala logaritmica
# plt.plot(num_digitos, times, 'o-')

plt.xlabel("Número de Dígitos (k)")
plt.ylabel("Tempo de Fatoração (s) - Em escala Log")
plt.title("Tempo vs. Número de Dígitos")
plt.grid(True)
plt.show()
