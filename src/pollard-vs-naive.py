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

def pollard(n):
    # Testando várias bases, quando necessário
    begin = time.time()
    bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31] 

    B = int(n**0.47) # limite para k (usaremos k!)

    for base in bases:
        a = base 
        for k in range(2, B + 1):
            a = pow(a, k, n) # a^k (mod n)
            d = math.gcd(a - 1, n)
            
            if 1 < d < n:
                end = time.time()
                return (d, n // d), end-begin
            
            elif d == n:
                print(f"  -> Falha com base {base} (MDC deu n). Trocando base...")
                break
    end = time.time()
    return (None, None), end-begin

random_semiprimes = [47053, 304679, 5494327, 76562491, 816359183, 
               2257234729, 36926403029, 831472422719, 
               6608034579161, 53177326426447, 640919985665423, 
               5550849765972349, 53033357137300961, 496121090393968057]

vulnerable_semiprimes = [38807, 139037, 2657621, 46628213, 117036793, 
               6361589687, 14069641051, 214106961829, 
               1392433829977, 24217699987267, 102537712225591, 
               1151394403072939, 75761282777688791, 172748749976857741]

def compare(semiprimes):
    timesN = []
    timesP = []
    
    for i in range(len(semiprimes)):
        divsN, timerN = naive(semiprimes[i])
        divsP, timerP = pollard(semiprimes[i])
        print(f"================================ {i+5} Dígitos ================================")
        print(f"Naive:   {semiprimes[i]} = {divsN[0]} x {divsN[1]}, tempo: {timerN}")
        print(f"Pollard: {semiprimes[i]} = {divsP[0]} x {divsP[1]}, tempo: {timerP}")
        timesN.append(timerN) 
        timesP.append(timerP) 
        
    timesN = np.array(timesN)
    timesP = np.array(timesP)

    num_digitos = np.array([len(str(n)) for n in semiprimes])

    plt.semilogy(num_digitos, timesN, 'o-', label="Método Naive")
    plt.semilogy(num_digitos, timesP, 'o-', label="Método de Pollard")
    #plt.plot(num_digitos, timesN, 'o-', label="Método Naive")
    #plt.plot(num_digitos, timesP, 'o-', label="Método de Pollard")

    plt.xlabel("Número de Dígitos (k)")
    plt.ylabel("Tempo de Fatoração (s) - Com escala Log")
    plt.title("Tempo vs. Número de Dígitos")
    plt.legend()
    
    plt.grid(True)
    plt.show()

# compare(random_semiprimes)
compare(vulnerable_semiprimes)