# Generators

# Q1

def permutations(lst):
    """Generates all permutations of sequence LST.  Each permutation is a
    list of the elements in LST in a different order.

    >>> sorted(permutations([1, 2, 3]))
    [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    >>> type(permutations([1, 2, 3]))
    <class 'generator'>
    >>> sorted(permutations((10, 20, 30)))
    [[10, 20, 30], [10, 30, 20], [20, 10, 30], [20, 30, 10], [30, 10, 20], [30, 20, 10]]
    >>> sorted(permutations("ab"))
    [['a', 'b'], ['b', 'a']]
    """

    if not lst:
        yield []
        return
    for perm in permutations(list(lst)[1:]):
        for i in range(len(lst)):
            yield perm[:i] + list(lst)[0:1] + perm[i:]


# Streams

class Stream:
    """A lazily computed linked list."""

    class empty:
        def __repr__(self):
            return 'Stream.empty'

    empty = empty()

    def __init__(self, first, compute_rest=lambda: Stream.empty):
        assert callable(compute_rest), 'compute_rest must be callable.'
        self.first = first
        self._compute_rest = compute_rest

    @property
    def rest(self):
        """Return the rest of the stream, computing it if necessary."""
        if self._compute_rest is not None:
            self._rest = self._compute_rest()
            self._compute_rest = None
        return self._rest

    def __repr__(self):
        return 'Stream({0}, <...>)'.format(repr(self.first))

def make_integer_stream(first=1):
    def compute_rest():
        return make_integer_stream(first+1)
    return Stream(first, compute_rest)

def map_stream(fn, s):
    if s is Stream.empty:
        return s
    return Stream(fn(s.first), lambda: map_stream(fn, s.rest))

def stream_to_list(s, n=10):
    """A list containing the elements of stream S,
    up to a maximum of N."""
    r = []
    while n > 0 and s is not Stream.empty:
        r.append(s.first)
        s = s.rest
        n -= 1
    return r
def filter_stream(fn, s):
    if s is Stream.empty:
        return s
    if fn(s.first):
        return Stream(s.first,lambda:filter_stream(fn,s.rest))
    else:
        return filter_stream(fn, s.rest)
# Q2

def scale_stream(s, k):
    """Return a stream of the elements of S scaled by a number K.

    >>> ints = make_integer_stream(1)
    >>> s = scale_stream(ints, 5)
    >>> stream_to_list(s, 5)
    [5, 10, 15, 20, 25]
    >>> s = scale_stream(Stream("x", lambda: Stream("y")), 3)
    >>> stream_to_list(s)
    ['xxx', 'yyy']
    >>> stream_to_list(scale_stream(Stream.empty, 10))
    []
    """
    if s is Stream.empty:
        return s
    else:
        return Stream(s.first * k,lambda:scale_stream(s.rest,k))

# Q3

def lst_to_stream(lst):
    """A utility for converting iterator or iterable LST into a corresponding
    Stream value.  (Use for testing only)"""
    if not lst:
        return Stream.empty
    return Stream(lst[0], lambda: lst_to_stream(lst[1:]))

def efficient_map_stream(fn, s):
    """Compute the Stream resulting from applying FN to each value of Stream
    S in turn.  [This implementation should only create a finite number of
    functions in total, regardless of the length of the stream S.]
    >>> str = lst_to_stream([7, -9, -3, 0])
    >>> ab = efficient_map_stream(abs, str)
    >>> stream_to_list(ab)
    [7, 9, 3, 0]
    >>> stream_to_list(efficient_map_stream(abs, Stream.empty))
    []
    >>> stream_to_list(efficient_map_stream(abs, Stream(-3)))
    [3]
    >>> stream_to_list(efficient_map_stream(lambda x: x*x, make_integer_stream(1)))
    [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
    """
    if s is Stream.empty:
        return s
    def compute_rest():
        return efficient_map_stream(fn, s.rest)
    return Stream(fn(s.first), compute_rest)


# Q4

temp = 0

def make_stream_of_streams():
    """
    >>> stream_of_streams = make_stream_of_streams()
    >>> stream_of_streams
    Stream(Stream(1, <...>), <...>)
    >>> stream_to_list(stream_of_streams, 3)
    [Stream(1, <...>), Stream(2, <...>), Stream(3, <...>)]
    >>> stream_to_list(stream_of_streams, 4)
    [Stream(1, <...>), Stream(2, <...>), Stream(3, <...>), Stream(4, <...>)]
    """
    global temp
    temp = temp + 1
    result = Stream(make_integer_stream(temp),lambda: make_stream_of_streams())
    return result

# Q5

def merge(s0, s1):
    """Return a stream over the elements of strictly increasing s0 and s1,
    removing repeats. Assume that s0 and s1 have no repeats.
    >>> ints = make_integer_stream(1)
    >>> twos = scale_stream(ints, 2)
    >>> threes = scale_stream(ints, 3)
    >>> m = merge(twos, threes)
    >>> stream_to_list(m,10)
    [2, 3, 4, 6, 8, 9, 10, 12, 14, 15]
    """
    if s0 is Stream.empty:
        return s1
    elif s1 is Stream.empty:
        return s0
    e0, e1 = s0.first, s1.first
    if e0 > e1:
        return Stream(e1,lambda:merge(s1.rest,s0))
    if e1 > e0:
        return Stream(e0,lambda:merge(s0.rest,s1))
    else:
        return Stream(e0,lambda:merge(s0.rest,s1.rest))

def make_s():
    """Return a stream over all positive integers with only factors 2, 3, & 5.

    >>> s = make_s()
    >>> stream_to_list(s, 20)
    [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 27, 30, 32, 36]
    """
    def rest():
        def only_the_factor(k):
            if k == 1:
                return True
            else:
                if k % 2 == 0:
                    return only_the_factor(k // 2)
                elif k % 3 == 0:
                    return only_the_factor(k // 3)
                elif k % 5 == 0:
                    return only_the_factor(k // 5)
                else:
                    return False

        the_new_stream1 = filter_stream(lambda x: only_the_factor(x),scale_stream(make_integer_stream(1),2))
        the_new_stream2 = filter_stream(lambda x: only_the_factor(x),scale_stream(make_integer_stream(1),3))
        the_new_stream3 = filter_stream(lambda x: only_the_factor(x),scale_stream(make_integer_stream(1),5))
        return merge(the_new_stream1,\
        merge(the_new_stream2,the_new_stream3))
    s = Stream(1, rest)
    return s
