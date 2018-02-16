import random


class Trade:
    def __init__(self, amount, owner):
        self.amount = amount
        self.owner = owner


class Market:
    def __init__(self, symbol='TAU', rate_range=(0.01, 0.02)):
        self.symbol = symbol
        self.rate_range = rate_range
        self.trades = []

    def get_rate(self):
        return random.randrange(self.rate_range)

    def get_trade(self, index):
        return self.trades[index]


class Exchange:
    def __init__(self):
        self.markets = []

    def add_market(self, market: Market):
        self.markets.append(market)

    def return_market(self, name):
        for m in self.markets:
            if m.symbol == name:
                return m
        return None


exchange = Exchange()
exchange.add_market(Market('TAU'))
exchange.add_market(Market('EOS'))
exchange.add_market(Market('ICX'))
exchange.add_market(Market('OMG'))

def purchase(m1, m2, amount):
    market_1 = exchange.return_market(m1)
    market_2 = exchange.return_market(m2)

    exchange_rate = market_1.get_rate()/market_2.get_rate()
    amount_to_fill = exchange_rate*amount
    filled = 0

    while filled < amount_to_fill:
        t = market_2.get_trade(0)
        if filled + t.amount < amount_to_fill:
            filled += t.amount
