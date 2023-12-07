from collections import Counter

input = '''
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
33332 0
2AAAA 0
77888 0
77788 0
77777 0
'''

input = open('2023/input7.txt', 'r').read()

cards = 'AKQJT98765432'

class Hand:
    def __init__(self, line):
        c, b = line.strip().split(' ')
        self.cards = c
        self.bid = int(b)
        self.counts = Counter(self.cards)
        self.countcounts = sorted(Counter(self.counts).values(), reverse=True)
        self.cardvals = [len(cards) - cards.index(l) for l in self.cards]

    def __repr__(self):
        return "Hand<{}, {}, {}>".format(
            self.cards,
            self.countcounts,
            self.cardvals,
        )
    
    def __lt__(self, other):
        if self.countcounts < other.countcounts:
            return True
        if self.countcounts > other.countcounts:
            return False
        return self.cardvals < other.cardvals
    
    def three_of_a_kind(self):
        return self.countcounts[0] == 3
        

hands = [Hand(line) for line in input.strip().split('\n')]
hands.sort()
score = 0
for i, h in enumerate(hands, 1):
    print(i, h)
    score += i * h.bid
print(score)