from lab03 import *

# Q9
def is_palindrome(n):
    """
    Fill in the blanks '_____' to check if a number
    is a palindrome.

    >>> is_palindrome(12321)
    True
    >>> is_palindrome(42)
    False
    >>> is_palindrome(2015)
    False
    >>> is_palindrome(55)
    True
    """
    x, y = n, 0
    f = lambda y: y * 10 + x % 10
    while x > 0:
        x, y =  x // 10, f(y)
    return y == n

# Q10
def ten_pairs(n):
    """Return the number of ten-pairs within positive integer n.

    >>> ten_pairs(7823952)
    3
    >>> ten_pairs(55055)
    6
    >>> ten_pairs(9641469)
    6
    """
    digit = []
    count = 0
    res = 0
    k, j, i , m = 0 , 0 , 0 , 0
    while n != 0:
        k = n % 10
        n = n // 10
        digit.append(k)
    while j < len(digit):
        while i < len(digit):
              if digit[i] + digit[j] == 10:
                  count = count + 1
              i = i + 1
        i = m + 1
        m = m + 1
        j = j + 1
    for x in digit:
        if x == 5:
            res = res + 1
    return count - res
