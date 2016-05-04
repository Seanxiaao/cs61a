test = {
  'name': 'Odds and Evens',
  'points': 0,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> class OddNaturalsIterator():
          ...     def __init__(self):
          ...         self.current = 1
          ...     def __next__(self):
          ...         result = self.current
          ...         self.current += 2
          ...         return result
          ...     def __iter__(self):
          ...         return self
          >>> odds = OddNaturalsIterator()
          >>> odd_iter1 = iter(odds)
          >>> odd_iter2 = iter(odds)
          >>> next(odd_iter1)
          1
          >>> next(odd_iter1)
          3
          >>> next(odd_iter1)
          5
          >>> next(odd_iter2)
          7
          >>> next(odd_iter1)
          9
          >>> next(odd_iter2)
          11
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> class EvenNaturalsIterator():
          ...     def __init__(self):
          ...         self.current = 0
          ...     def __next__(self):
          ...         result = self.current
          ...         self.current += 2
          ...         return result
          ...     def __iter__(self):
          ...         return EvenNaturalsIterator()
          >>> evens = EvenNaturalsIterator()
          >>> even_iter1 = iter(evens)
          >>> even_iter2 = iter(evens)
          >>> next(even_iter1)
          0
          >>> next(even_iter1)
          2
          >>> next(even_iter1)
          4
          >>> next(even_iter2)
          0
          >>> next(even_iter2)
          2
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': False,
      'type': 'wwpp'
    }
  ]
}
