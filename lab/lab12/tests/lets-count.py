test = {
  'name': 'lets-count',
  'points': 0,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          sqlite> SELECT * from fa15favnum;
          7|35
          sqlite> SELECT * from fa15favpets;
          dog|49
          cat|19
          tiger|17
          |15
          dragon|12
          panda|11
          monkey|8
          wolf|8
          cheetah|6
          lion|6
          sqlite> SELECT * from sp16favpets;
          |17
          dragon|15
          dog|13
          paul hilfinger|10
          pikachu|7
          cat|6
          unicorn|6
          chinchilla|5
          phoenix|5
          puppy|5
          sqlite> SELECT * from sp16dragon;
          dragon|15
          sqlite> SELECT * from sp16alldragons;
          dragon|28
          sqlite> SELECT * from obedienceimage;;
          7||1
          7|Image 1|42
          7|Image 2|18
          7|Image 3|14
          7|Image 4|27
          7|Image 5|24
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
