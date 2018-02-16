import random
import uuid
import pprint

EOS = 'EOS'
ICX = 'ICX'
OMG = 'OMG'

TAU = 'TAU'
MM = 'MM'

tokens = [EOS, ICX, OMG]
owners = [uuid.uuid4().hex for x in range(100)]

EOSBucket = {
    'token': EOS,
    'trades': []
}

ICXBucket = {
    'token': ICX,
    'trades': []
}

OMGBucket = {
    'token': OMG,
    'trades': []
}

staking_bucket = {
    'token': TAU,
    'trades': []
}


def get_rate_for(token):
    if token == EOS:
        return random.uniform(0.002, 0.003)
    elif token == ICX:
        return random.uniform(0.0005, 0.0007)
    elif token == OMG:
        return random.uniform(0.01, 0.015)
    elif token == TAU:
        return random.uniform(0.007, 0.0085)
    else:
        return 0


def make_trade():
    token_selection = random.sample(tokens, 2)
    return {
        'sell': token_selection[0],
        'buy': token_selection[1],
        'amount': random.randint(1, 100),
        'owner': random.sample(owners, 1)[0]
    }


fake_trades = [make_trade() for i in range(100)]
staking_bucket['trades'] = [{
    'sell': TAU,
    'buy': MM,
    'amount': random.randint(1, 100),
    'owner': random.sample(owners, 1)[0]
} for j in range(100)]

for trade in fake_trades:
    # determine how much tau to buy
    token_to_tau_rate = get_rate_for(trade['sell'])/get_rate_for(TAU)
    tau_needed = token_to_tau_rate

    # pop values from the stack until all tau needed is purchased
    filled = 0
    for t in staking_bucket['trades']:*trade['amount']
        # can't modify
        if t['amount'] > 0:
            if filled + t['amount'] < tau_needed:
                filled += t['amount']
                t['amount'] = 0
                staking_bucket['trades'].remove(i)
                i += 1
                print('{} of {} filled'.format(filled, tau_needed))
                print('Trade removed!\n')
            else:
                t['amount'] -= tau_needed - filled
                filled = tau_needed
                print('{} of {} filled'.format(filled, tau_needed))
                break


def process_trade(t):
    tau_needed = (get_rate_for(trade['sell'])/get_rate_for(TAU))*trade['amount']
    filled = 0
    i = 0
    while filled < t['amount']:
        if len(staking_bucket['trades']) > 0:
            s = staking_bucket['trades'].pop(0)
            if filled + s['amount'] < tau_needed:

        else:
            break

    #print(tau_needed)