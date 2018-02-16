import random
import secrets

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


def random_stake():
    return {
        'amount': random.randint(10, 50),
        'owner': random.sample(wallets, 1)[0],
        'id': secrets.token_hex(8)
    }


major_liquid = [random_stake() for x in range(100)]

tx = {'amount': None, 'owner': None, 'id': None}

minor_liquid = {
    'EOS': [],
    'ICX': [],
    'OMG': []
}

def tx_in(token, tx):

    # determine the forex exchange rate between the base currency
    # and major liquid market
    fx = token/return_rate()

    # setup how much to fill and the out transaction for when it is filled
    to_fill = fx * tx['amount']
    filled = 0
    out_tx = {'amount': 0, 'owner': tx['owner'], 'id': secrets.token_hex(8)}

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
            to_give = to_fill / ml['amount']

            # calculate the value in tokens
            to_give /= fx

            # shoot off a transaction to illiquid which attempts to fill it there (potential recursion here)

            # destroy the order
            major_liquid.pop(0)

        else:
            # otherwise, the entire trade could not be liquidated and we have to alter is slightly
            difference = to_fill - filled
            ml['amount'] -= difference

            to_give = to_fill / difference
            to_give /= fx

            # shoot off a transaction to illiquid which attempts to fill it there (potential recursion here)


def return_rate():
    return 1