#############
# Iterators #
#############

# Q2
class IteratorRestart:
    """
    >>> iterator = IteratorRestart(2, 7)
    >>> for num in iterator:
    ...     print(num)
    2
    3
    4
    5
    6
    7
    >>> for num in iterator:
    ...     print(num)
    2
    3
    4
    5
    6
    7
    """
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __next__(self):
        if self.start > self.end:
            raise StopIteration
        itered = self.start
        self.start += 1
        return itered

    def __iter__(self):
        return IteratorRestart(self.start,self.end)

# Q4
class Str:
    """
    >>> s = Str("hello")
    >>> for char in s:
    ...     print(char)
    ...
    h
    e
    l
    l
    o
    >>> for char in s:    # a standard iterator does not restart
    ...     print(char)
    """
    def __init__(self, string):
        self.string = list(string)

    def __next__(self):
        if len(self.string) == 0:
            raise StopIteration
        itered = self.string[0]
        self.string = self.string[1:]
        return itered

    def __iter__(self):
        return self
##############
# Generators #
##############

# Q6
def countdown(n):
    """
    >>> from types import GeneratorType
    >>> type(countdown(0)) is GeneratorType # countdown is a generator
    True
    >>> for number in countdown(5):
    ...     print(number)
    ...
    5
    4
    3
    2
    1
    0
    """
    while n >= 0:
        yield n
        n += -1

class Countdown:
    """
    >>> from types import GeneratorType
    >>> type(Countdown(0)) is GeneratorType # Countdown is an iterator
    False
    >>> for number in Countdown(5):
    ...     print(number)
    ...
    5
    4
    3
    2
    1
    0
    """
    def __init__(self, number):
        self.number = number

    def __next__(self):
        while self.number < 0:
            raise StopIteration
        itered = self.number
        self.number += -1
        return itered

    def __iter__(self):
        return self

# Q7
def hailstone(n):
    """
    >>> for num in hailstone(10):
    ...     print(num)
    ...
    10
    5
    16
    8
    4
    2
    1
    """
    while n >= 1:
        yield n
        if n == 1:
            return 1
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
