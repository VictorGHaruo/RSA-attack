import random
import math
from wiener_utils import *
from wiener_attack import wiener_attack


# -------------------------------------------------------------

def generate_prime(bits: int) -> int:
    """Gera um inteiro ímpar aleatório do tamanho correto em bits e verifica primalidade por força bruta.
       (Suficiente para testes; não destinado a ser criptograficamente forte.)
    """
    while True:
        x = random.getrandbits(bits) | 1  # force que seja ímpar
        if is_probably_prime(x):
            return x

def is_probably_prime(n: int, rounds: int = 20) -> bool:
    """Teste de primalidade Miller-Rabin."""
    if n < 2:
        return False
    # primos pequenos
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    for sp in small_primes:
        if n == sp:
            return True
        if n % sp == 0:
            return n == sp

    # seja n-1 = 2^s * d
    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2

    for _ in range(rounds):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for __ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


# -------------------------------------------------------------

def test_invmod_basic():
    assert invmod(3, 11) == 4  # 3*4 = 12 = 1 mod 11
    assert invmod(10, 17) == 12
    assert invmod(2, 4) is None  # gcd != 1

def test_is_perfect_square():
    assert is_perfect_square(0)
    assert is_perfect_square(1)
    assert is_perfect_square(49)
    assert not is_perfect_square(50)
    assert not is_perfect_square(-9)

def test_continued_fraction_simple():
    cf = continued_fraction(355, 113)
    assert cf == [3, 7, 16]

def test_convergents():
    cf = [3, 7, 16]  # 355/113
    conv = list(convergents(cf))
    assert conv[-1] == (355, 113)


# -------------------------------------------------------------
# Testes para o ataque de Wiener
# -------------------------------------------------------------

def test_wiener_attack_weak_key_small():
    """Teste se o ataque de Wiener funciona em uma chave RSA pequena/fraca.
    """
    p = 349
    q = 367
    N = p * q
    phi = (p - 1) * (q - 1)

    d = 5
    e = invmod(d, phi)
    assert e is not None

    recovered = wiener_attack(N, e)
    assert recovered == d


def test_wiener_attack_strong_key_fails():
    """Teste se o Wiener attack falha quando d é grande/seguro.
    """
    p = generate_prime(16)
    q = generate_prime(16)
    N = p * q
    phi = (p - 1) * (q - 1)

    # escolha d grande (seguro), inverta para obter e
    while True:
        d = random.randint(phi // 4, phi - 1)
        if math.gcd(d, phi) == 1:
            break

    e = invmod(d, phi)
    assert e is not None

    recovered = wiener_attack(N, e)
    assert recovered is None


def test_wiener_attack_random_weak_keys():
    """Crie muitas chaves RSA fracas aleatórias com d < N^(1/4)/3.
    Wiener deve sempre ter sucesso.
    """
    for _ in range(10):
        p = generate_prime(32)
        q = generate_prime(32)
        N = p * q
        phi = (p - 1) * (q - 1)

        # limite superior para vulnerabilidade de Wiener
        bound = int(N**0.25) // 3
        if bound < 5:
            continue

        # escolha um pequeno d aleatório < bound
        while True:
            d = random.randint(5, bound)
            if math.gcd(d, phi) == 1:
                break

        e = invmod(d, phi)
        assert e is not None

        recovered = wiener_attack(N, e)
        assert recovered == d


def test_wiener_attack_edge_case_k_zero():
    """Construa um caso onde o primeiro convergente tem k=0 (deve ser ignorado).
    """
    # Este caso artificial garante (e,N) tal que e < N
    # dá um primeiro convergente k=1, d=N//e, mas para controlabilidade:
    N = 101 * 113
    e = 1  # isso torna o primeiro convergente estranho, mas sintaticamente válido

    # O ataque não deve travar
    result = wiener_attack(N, e)
    # e=1 implica que o expoente privado é sempre 1
    # mas o ataque de Wiener normalmente falha com e muito pequeno
    assert result in (1, None)


def test_wiener_attack_no_false_positives():
    """Se o ataque encontrar um d, ele deve realmente satisfazer ed ≡ 1 mod φ(N).
    """
    p = generate_prime(32)
    q = generate_prime(32)
    N = p * q
    phi = (p - 1) * (q - 1)

    # escolha um pequeno d com gcd=1
    d = random.randint(5, min(50, phi - 1))
    while math.gcd(d, phi) != 1:
        d = random.randint(5, min(50, phi - 1))

    e = invmod(d, phi)
    assert e is not None

    recovered = wiener_attack(N, e)

    if recovered is not None:
        # deve realmente ser o d correto
        assert (e * recovered - 1) % phi == 0
