import math
import time
import numpy as np
import matplotlib.pyplot as plt

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
        print(x)
        w = pow(x, 2) - N
        y = math.isqrt(w)
        if (y*y  == w):
            end = time.time()
            return (x-y, x+y), end-begin

    return (1, N), end-begin


# print(fermat(107899431))
semiprimesC = [15, 143, 2491, 47053, 304679, 5494327, 76562491, 816359183]
semiprimesF = [93, 267, 1569, 19473, 499461, 2899473, 17899473, 107899431]


def compare(semiprimesF, semiprimesC):
    timesC = []
    timesF = []
    for i in range(len(semiprimesC)):
        divsF, timerF = fermat(semiprimesF[i])
        divsC, timerC = fermat(semiprimesC[i])
        timesC.append(timerC)
        timesF.append(timerF)
    timesC = np.array(timesC)
    timesF = np.array(timesF)

    num_digitos = np.array([len(str(n)) for n in semiprimesC])
    # plt.semilogy(num_digitos, timesC, 'o-')
    # plt.semilogy(num_digitos, timesF, 'o-')

    # Plota Gráfico sem escala logaritmica
    plt.plot(num_digitos, timesC, 'o-')
    plt.plot(num_digitos, timesF, 'o-')

    plt.xlabel("Número de Dígitos (k)")
    plt.ylabel("Tempo de Fatoração (s) - Sem escala Log")
    plt.title("Tempo vs. Número de Dígitos")
    plt.grid(True)
    plt.show()

# semiprimesC=[15, 143, 2491, 47053, 304679, 5494327, 76562491]
# semiprimesF=[93, 267, 1569, 19473, 499461, 2899473, 17899473]
compare(semiprimesF, semiprimesC)
