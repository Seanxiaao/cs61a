test = {
  'name': 'matchmaker',
  'points': 0,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          sqlite> SELECT * FROM matchmaker LIMIT 10;
          dog|Hello|blue|blue
          dog|Work|green|black
          dragon|Sandstorm|black|black
          |Work|citrine|green
          tiger||purple|blue
          dog|Fur Elise|gray|red
          dog|Fur Elise|gray|light blue
          doge|Sandstorm|brown|blue
          paul hilfinger|Sandstorm|69|blue
          paul hilfinger|Sandstorm|69|blurpul
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'ordered': False,
      'scored': True,
      'setup': r"""
      sqlite> .read lab12.sql
      """,
      'teardown': '',
      'type': 'sqlite'
    }
  ]
}
