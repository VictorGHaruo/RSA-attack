import math
from random import random, choice
from typing import Optional
from wiener_utils import (
    invmod,
    is_perfect_square,
    continued_fraction,
    convergents,
)

def wiener_attack(N: int, e: int, verbose: bool = False) -> Optional[int]:
    """Tenta reconstruir o expoente privado d para recuperar o expoente privado RSA
    d usando o ataque de Wiener.

    O ataque de Wiener funciona quando o expoente privado satisfaz:
        d < N**(1/4) / 3
    (ou aproximadamente d = O(N^1/4))

    O ataque
    --------
    1 - Compute a expansão em fração contínua de e/N.
    2 - Enumere todos os convergentes k/d dessa expansão.
        Se d for o verdadeiro expoente privado RSA, então:
            ed ≡ 1 (mod φ(N)),
        portanto:
            (e*d - 1) / k = φ(N)
    3 - A partir de φ(N) calculamos:
           s = p + q = N - φ(N) + 1
       e verificamos se a equação quadrática:
           x^2 - s x + N = 0
       possui soluções inteiras.
    4. Se p e q válidos forem encontrados, recalculamos φ(N) e
       verificamos se invmod(e, φ(N)) existe.
    5. Se tudo for bem-sucedido, retorne o verdadeiro d. Caso contrário, retorne None.

    Parâmetros
    ----------
    N : int
        Inteiro RSA (produto de dois primos p e q).
    e : int
        Expoente público RSA.
    verbose : bool, optional
        Se True, imprime saída diagnóstica detalhada.
    
    Retornos
    --------
    int or None
        O expoente privado d recuperado, ou None se o ataque falhar.
    """

    # 1 - compute a expansão em fração contínua de e/N
    cf = continued_fraction(e, N)

    # 2 - itere sobre os convergentes (k/d)
    for idx, (k, d) in enumerate(convergents(cf)):
        if verbose:
            print(f"\n[convergente {idx}] k={k}, d={d}")

        # Um convergente com k = 0 não pode produzir φ(N) válido
        if k == 0:
            if verbose:
                print("  rejeitado: k=0")
            continue

        # Verifique se (e*d - 1) é divisível por k.
        # Se assim for, φ(N) = (e*d - 1)/k é um inteiro.
        if (e * d - 1) % k != 0:
            if verbose:
                print("  rejeitado: (e*d - 1) % k != 0")
            continue

        phi_candidate = (e * d - 1) // k
        if verbose:
            print(f"  phi_candidate = {phi_candidate}")

        # Compute s = p + q usando a identidade:
        #       φ(N) = (p - 1)(q - 1) = N - (p + q) + 1
        #  =>   p + q = N - φ(N) + 1
        s = N - phi_candidate + 1

        # O discriminante de x^2 - s x + N deve ser um quadrado perfeito:
        #       Δ = s^2 - 4N
        Delta = s**2 - 4 * N
        if not is_perfect_square(Delta):
            if verbose:
                print("  rejeitado: discriminante não é um quadrado perfeito")
            continue

        t = int(math.isqrt(Delta))

        # Raízes da equação quadrática:
        p = (s + t) // 2
        q = (s - t) // 2

        # Verificações de sanidade nas raízes
        if p <= 1 or q <= 1:
            if verbose:
                print("  rejeitado: p ou q não positivos")
            continue

        if p * q != N:
            if verbose:
                print("  rejeitado: p*q != N")
            continue

        # Neste ponto, (p, q) são os primos RSA reais; calcule o verdadeiro φ(N)
        phi = (p - 1) * (q - 1)
        d_real = invmod(e, phi)

        if d_real is None:
            # Isso seria extremamente incomum se p, q estiverem corretos
            if verbose:
                print("  rejeitado: invmod(e, phi) falhou (!)")
            continue

        if verbose:
            print("  SUCESSO: p, q, d recuperados")
        return d_real

    # Se nenhum convergente produzir (p, q) válidos, o ataque falha
    if verbose:
        print("  FALHA: nenhum p, q, d recuperado")
    return None

if __name__ == "__main__":
    p = int(input("Insira p: "))
    q = int(input("Insira q: "))
    d = int(input("Insira d (ou 0 para automático): "))
    N = p * q
    phi = (p-1) * (q-1)
    bound = int(N**0.25) // 3
    
    if d == 0:
        while math.gcd(d, phi) != 1:
            d = choice(range(2, bound))
    e = invmod(d, phi)

    print("-"*60 + "\nTestando Wiener com:")
    print(f"  p = {p}; q = {q}")
    print(f"  N = {N}; φ(N) = {phi}; cota = {bound}")
    print(f"  e = {e}")
    print(f"  d = {d}; e*d = {e*d % phi} mod φ(N)")

    recovered_d = wiener_attack(N, e, verbose=True)
    print("-"*60 + f"\nRecuperado: d = {recovered_d}")
