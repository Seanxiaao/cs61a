test = {
  'name': 'composites',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          sqlite> select * from composites order by c;
          4
          6
          8
          9
          10
          12
          14
          15
          16
          18
          20
          21
          22
          24
          25
          26
          27
          28
          30
          32
          33
          34
          35
          36
          38
          39
          40
          42
          44
          45
          46
          48
          49
          50
          51
          52
          54
          55
          56
          57
          58
          60
          62
          63
          64
          65
          66
          68
          69
          70
          72
          74
          75
          76
          77
          78
          80
          81
          82
          84
          85
          86
          87
          88
          90
          91
          92
          93
          94
          95
          96
          98
          99
          100
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'ordered': False,
      'scored': True,
      'setup': r"""
      sqlite> .read hw08.sql
      """,
      'teardown': '',
      'type': 'sqlite'
    }
  ]
}
