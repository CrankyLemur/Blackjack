class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    def __repr__(self):
        if self.suit == 'clubs':
            return (f"""\
.------.
|{self.rank:<2}--  |
| :(): |
| ()() |
|  --{self.rank:>2}|
`------'\
""")
        if self.suit == 'diamonds':
            return (f"""\
.------.
|{self.rank:<2}--  |
| :/\: |
| :\/: |
|  --{self.rank:>2}|
`------'\
""")
        if self.suit == 'hearts':
            return (f"""\
.------.
|{self.rank:<2}--  |
| (\/) |
|  \/  |
|  --{self.rank:>2}|
`------'\
""")
        if self.suit == 'spades':
            return (f"""\
.------.
|{self.rank:<2}--  |
|  /\  |
| (__) |
|  --{self.rank:>2}|
`------'\
""")
        else:
            return ("""\
.------.
|  --, |
|  ,_| |
|  |   |
|  .   |
`------'\
""")