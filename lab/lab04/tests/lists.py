test = {
  'name': 'List Comprehension',
  'points': 0,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> [x*x for x in range(5)]
          [0, 1, 4, 9, 16]
          >>> [n for n in range(10) if n % 2 == 0]
          [0, 2, 4, 6, 8]
          >>> ones = [1 for i in ["hi", "bye", "you"]]
          >>> ones + [str(i) for i in [6, 3, 8, 4]]
          [1, 1, 1, '6', '3', '8', '4']
          >>> [i+5 for i in [n for n in range(1,4)]]
          [6, 7, 8]
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