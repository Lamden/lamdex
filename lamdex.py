import random
import secrets
import requests

'''

    __    ___    __  _______  _______  __
   / /   /   |  /  |/  / __ \/ ____/ |/ /
  / /   / /| | / /|_/ / / / / __/  |   / 
 / /___/ ___ |/ /  / / /_/ / /___ /   |  
/_____/_/  |_/_/  /_/_____/_____//_/|_|  

Major liquid market is always TAU
Minor liquid market is always a supported token

IN_TXs turn a token into tau
OUT_TXs turn tau into a token

A TX is split into an input and an output fulfilled in two parts.

1. fill the liquid market with a bunch of stake trades

'''

wallets = [secrets.token_hex(4) for x in range(10)]
supported_tokens = ['EOS', 'ICX', 'OMG', 'TAU']


def random_stake(rng=(10, 50)) -> dict:
    return {
        'amount': random.randint(rng[0], rng[1]),
        'owner': random.sample(wallets, 1)[0],
        'id': secrets.token_hex(8)
    }


major_liquid = [random_stake() for x in range(100)]

minor_liquid = {
    'EOS': [],
    'ICX': [],
    'OMG': []
}


def fill_tx():
    pass


def build_tx():
    pass


def tx_in(token_sell, token_buy, tx):

    # determine the forex exchange rate between the base currency
    # and major liquid market

    fx = forex(token_sell, 'TAU')

    print(fx)

    # setup how much to fill and the out transaction for when it is filled
    to_fill = tx['amount'] * fx
    filled = 0
    out_tx = {'amount': 0, 'owner': tx['owner'], 'id': secrets.token_hex(8)}

    print('attempting to liquidate {} {} for TAU\n'.format(tx['amount'], token_sell))

    # try to completely fill the order with the current major liquid
    while filled < to_fill:
        # iterate through the queue and fill each order
        ml = major_liquid[0]

        # check if the entire order can be consumed
        if filled + ml['amount'] < to_fill:

            # if so, add the amount to the fill and out tx (is that redundant?)
            filled += ml['amount']
            out_tx['amount'] += ml['amount']

            # calculate how much to give the major liquid holder
            to_give = ml['amount'] / fx

            # shoot off a transaction to illiquid which attempts to fill it there (potential recursion here)
            print('complete: {} {} sold, {} TAU bought'.format(to_give, token_sell, ml['amount']))
            print('{}/{} left to liquidate'.format(filled, to_fill))
            print('sending to minor markets\n')

            # destroy the order
            major_liquid.pop(0)

        else:
            # otherwise, the entire trade could not be liquidated and we have to alter is slightly
            print('partial: liquidation of {}'.format(ml))
            difference = to_fill - filled
            ml['amount'] -= difference

            filled += difference
            out_tx['amount'] += difference

            print('only {} liquidated'.format(difference))

            to_give = to_fill / difference
            to_give /= fx

            # shoot off a transaction to illiquid which attempts to fill it there (potential recursion here)

            print('sending to minor markets\n')

            # lets redundantly break just in case
            break

    print('sending out tx. buying {} with {} TAU'.format(token_buy, out_tx['amount']))
    print(out_tx)


def tx_out(token, tx):
    pass


def forex(token_a, token_b, test=False):
    if test is True:
        return 1
    return return_rate(token_a)/return_rate(token_b)


def return_rate(token: str, test: bool = False) -> float:
    if test is True:
        return 1
    assert token in supported_tokens, 'Pass a supported token: {}'.format(supported_tokens)
    url = 'https://api.hitbtc.com/api/2/public/ticker/{}BTC'.format(token)
    r = requests.get(url)
    return float(r.json()['last'])

if __name__ == "__main__":
    tx_in('EOS', 'ICX', random_stake((10, 20)))