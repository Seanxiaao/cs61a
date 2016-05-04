test = {
  'name': 'smallest-int-count',
  'points': 0,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          sqlite> SELECT * FROM smallest_int_count LIMIT 50;
          1|39
          2|12
          3|8
          4|11
          5|4
          6|5
          7|5
          8|8
          9|6
          10|2
          11|11
          12|9
          13|6
          14|9
          15|1
          16|5
          17|10
          18|4
          19|9
          20|1
          22|3
          23|10
          24|4
          25|2
          26|4
          27|2
          28|1
          29|3
          30|1
          31|3
          32|2
          33|3
          34|3
          36|1
          37|4
          38|2
          39|1
          41|4
          42|2
          43|2
          44|2
          45|1
          46|1
          49|1
          51|4
          53|5
          54|2
          55|1
          57|1
          58|1
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'ordered': False,
      'scored': True,
      'setup': r"""
      sqlite> .read lab12_extra.sql
      """,
      'teardown': '',
      'type': 'sqlite'
    }
  ]
}
