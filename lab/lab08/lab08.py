## Sets + Orders of Growth ##

# Q2
def find_duplicates(lst):
    """Returns True if lst has any duplicates and False if it does not.

    >>> find_duplicates([1, 2, 3, 4, 5])
    False
    >>> find_duplicates([1, 2, 3, 4, 2])
    True
    >>> find_duplicates(list(range(100000)) + [-1]) # make sure you have linear time
    False
    """
    return  len(set(lst)) < len(lst)


# Q3
def pow(n,k):
    """Computes n^k.

    >>> pow(2, 3)
    8
    >>> pow(4, 2)
    16
    >>> a = pow(2, 100000000) # make sure you have log time
    """
    result=1
    while k:
        if (k&1):
            result *= n
        n *= n
        k >>= 1 #to use the bin method
    return result
