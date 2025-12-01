import matplotlib.pyplot as plt
import numpy as np
import time
import math

def naive(n):
    begin = time.time()
    div = []
    while (n%2 == 0):
        div.append(2)
        n = n//2
    i = 3
    while i*i <= n:
        # print(i)            
        while n%i == 0:
            div.append(i)
            n = n//i
        i = i + 2

    end = time.time()
    if n > 1:
        div.append(n)
    return div, end-begin

def fermat(N):
    begin = time.time()
    x = math.isqrt(N)
    
    if (N%2 == 0):
        end = time.time()
        return (2, N//2), end-begin

    if (x*x == N):
        end = time.time()
        return (x, x), end-begin

    while x != (N + 1)//2:
        x = x + 1
        # print(x)
        w = pow(x, 2) - N
        y = math.isqrt(w)
        if (y*y  == w):
            end = time.time()
            return (x-y, x+y), end-begin

    return (1, N), end-begin

semiprimesC = [15, 143, 2491, 47053, 304679, 5494327, 76562491, 816359183]
semiprimesF = [93, 267, 1569, 19473, 499461, 2899473, 17899473, 107899431]

def compare(semiprimes):
    timesN = []
    timesF = []
    
    for i in range(len(semiprimes)):
        divsF, timerN = naive(semiprimes[i])
        divsC, timerC = fermat(semiprimes[i])
        timesN.append(timerN) 
        timesF.append(timerC) 
        
    timesN = np.array(timesN)
    timesF = np.array(timesF)

    num_digitos = np.array([len(str(n)) for n in semiprimes])

    # plt.semilogy(num_digitos, timesN, 'o-', label="Método Naive")
    # plt.semilogy(num_digitos, timesF, 'o-', label="Método de Fermat")
    plt.plot(num_digitos, timesN, 'o-', label="Método Naive")
    plt.plot(num_digitos, timesF, 'o-', label="Método de Fermat")

    plt.xlabel("Número de Dígitos (k)")
    plt.ylabel("Tempo de Fatoração (s) - Sem escala Log")
    plt.title("Tempo vs. Número de Dígitos")
    plt.legend()
    
    plt.grid(True)
    plt.show()
compare(semiprimesC)
