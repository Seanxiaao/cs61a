"""Optional program for lab02 """

from lab02 import *
i = 0
# Extra Question
def hailstone(n):
    """Print out the hailstone sequence starting at n, and return the
    number of elements in the sequence.

    >>> a = hailstone(10)
    10
    5
    16
    8
    4
    2
    1
    >>> a
    7
    """
    global i
    i = i + 1
    print(int(n))
    if n == 1:
        return i
    else:
        if n % 2 == 0:
            n = n / 2
        else:
            n = 3 * n + 1
    return hailstone(n)



def count_cond(condition):
    """
    >>> count_factors = count_cond(lambda n, i: n % i == 0)
    >>> count_factors(2) # 1, 2
    2
    >>> count_factors(4) # 1, 2, 4
    3
    >>> count_factors(12) # 1, 2, 3, 4, 6, 12
    6

    >>> is_prime = lambda n, i: count_factors(i) == 2
    >>> count_primes = count_cond(is_prime)
    >>> count_primes(2) # 2
    1
    >>> count_primes(3) # 2, 3
    2
    >>> count_primes(4) # 2, 3
    2
    >>> count_primes(5) # 2, 3, 5
    3
    >>> count_primes(20) # 2, 3, 5, 7, 11, 13, 17, 19
    8
    """
    def counter(n):
        i ,count = 1, 0
        while i <= n:
            if condition:
                count += 1
            i += 1
        return count
    return counter

def cycle(f1, f2, f3):
    """ Returns a function that is itself a higher order function
    >>> def add1(x):
    ...     return x + 1
    >>> def times2(x):
    ...     return x * 2
    >>> def add3(x):
    ...     return x + 3
    >>> my_cycle = cycle(add1, times2, add3)
    >>> identity = my_cycle(0)
    >>> identity(5)
    5
    >>> add_one_then_double = my_cycle(2)
    >>> add_one_then_double(1)
    4
    >>> do_all_functions = my_cycle(3)
    >>> do_all_functions(2)
    9
    >>> do_more_than_a_cycle = my_cycle(4)
    >>> do_more_than_a_cycle(2)
    10
    >>> do_two_cycles = my_cycle(6)
    >>> do_two_cycles(1)
    19
    """
    i = 0
    a = lambda n : n // 3
    b = lambda n : n % 3
    def h(x):
        return f3(f2(f1))
    def q(x):
        return f2(f1)
    while i <= a:
        h = h(h)
        i = i + 1
    if n % 3 == 0:
        return lambda x:h(x)
    if n % 3 == 1:
        return lambda x:f1(h(x))
    if n % 3 == 2:
        return lambda x:q(h(x))


def paths(m, n):
    """Return the number of paths from one corner of an
    M by N grid to the opposite corner.

    >>> paths(2, 2)
    2
    >>> paths(5, 7)
    210
    >>> paths(117, 1)
    1
    >>> paths(1, 157)
    1
    """
    if m == 1 or n == 1:
        return 1
    else:
        return paths(m-1,n) + paths(m,n-1)
