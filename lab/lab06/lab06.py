## Lab 6: OOP and Nonlocal ##

# Question 1
def vending_machine(snacks):
    """Cycles through list of snacks.

    >>> vender = vending_machine(['chips', 'chocolate', 'popcorn'])
    >>> vender()
    'chips'
    >>> vender()
    'chocolate'
    >>> vender()
    'popcorn'
    >>> vender()
    'chips'
    >>> other = vending_machine(['brownie'])
    >>> other()
    'brownie'
    >>> vender()
    'chocolate'
    """
    count = -1
    def count_snacks():
        nonlocal snacks
        nonlocal count
        count += 1
        if count % 3 == 0:
            count = 0
        return snacks[count]
    return count_snacks
