import math
from typing import Optional, Tuple


def egcd(a: int, b: int) -> Tuple[int, int, int]:
    """Computa o Algoritmo Euclidiano Estendido.

    Dados inteiros a e b, retorna uma tupla (g, x, y) tal que:
        g = gcd(a, b)
        x, y satisfazem:  a*x + b*y = g

    Isso é usado para calcular inversos modulares.
    Parâmetros
    ----------
    a : int
        Primeiro inteiro.
    b : int
        Segundo inteiro.

    Retornos
    --------
    (g, x, y) : tuple[int, int, int]
        g = gcd(a, b)
        x, y são coeficientes de Bézout.
    """
    if b == 0:
        return (a, 1, 0)
    
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)

def invmod(a: int, m: int) -> Optional[int]:
    """Computa o inverso modular de a módulo m, se existir.

    O inverso modular é o inteiro x tal que:
        a*x ≡ 1 (mod m)

    Ele existe se e somente se gcd(a, m) = 1.

    Parâmetros
    ----------
    a : int
        O número a ser invertido módulo m.
    m : int
        O módulo.

    Retornos
    --------
    int or None
        O inverso modular x no intervalo [0, m-1], ou None se gcd(a, m) != 1.
    """
    g, x, _ = egcd(a, m)
    if g != 1:
        return None
    return x % m

def is_perfect_square(n):
    """Determina se um inteiro é um quadrado perfeito.

    Parâmetros
    ----------
    n : int
        Número a ser testado.

    Retornos
    --------
    bool
        True se n é um quadrado perfeito, False caso contrário.
    """
    if n < 0:
        return False
    r = int(math.isqrt(n))
    return r*r == n

def continued_fraction(a, b):
    """Computa a expansão em fração contínua de a/b.
    Retorna a lista de quocientes parciais [a0, a1, ..., an]
    tal que:
        a/b = a0 + 1/(a1 + 1/(a2 + ...))

    Parâmetros
    ----------
    a : int
        Numerador.
    b : int
        Denominador.

    Retornos
    --------
    list[int]
        A sequência de coeficientes da fração contínua.
    """
    cf = []
    while b != 0:
        q = a // b
        cf.append(q)
        a, b = b, a - q*b
    return cf

def convergents(cf):
    """
    Gera convergentes sucessivos a partir de uma fração contínua.

    Cada convergente é um número racional p/q que aproxima o número original.

    Usa a recorrência:
        p[n] = a[n] * p[n-1] + p[n-2]
        q[n] = a[n] * q[n-1] + q[n-2]
    onde a[n] são os coeficientes da fração contínua.

    Parâmetros
    ----------
    cf : list[int]
        Coeficientes da fração contínua.

    Gerações
    --------
    (p, q) : tuple[int, int]
        O numerador e denominador de cada convergente.
    """
    p_prev2, p_prev1 = 1, cf[0]
    q_prev2, q_prev1 = 0, 1
    yield (cf[0], 1)
    for a in cf[1:]:
        p = a * p_prev1 + p_prev2
        q = a * q_prev1 + q_prev2
        yield (p, q)
        p_prev2, p_prev1 = p_prev1, p
        q_prev2, q_prev1 = q_prev1, q
