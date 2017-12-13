import collections
import json
import time

from poloniex import Poloniex

COMMISSION = 0.0025

CONFIG_FILE = 'resources/pairs.json'
MAIN_ACTIVE = ['BTC', 'ETH']


def split(str):
    return str.split('_')


def coin_pairs():
    with open(CONFIG_FILE) as file_data:
        data = json.load(file_data)

    return data


def create_dictionary(pairs, ticker):
    dictionary = collections.defaultdict(dict)
    for pair in pairs:
        p = pair.upper()
        src, dst = split(p)

        src_ask = ticker[p]['lowestAsk']
        src_bid = ticker[p]['highestBid']

        dictionary[src][dst] = float(src_ask)
        dictionary[dst][src] = 1 / float(src_bid)

    return dictionary


while True:
    polo = Poloniex()
    pairs = coin_pairs()
    ticker = polo.returnTicker()
    currencies = create_dictionary(pairs, ticker)

    print('.')

    for active in MAIN_ACTIVE:
        for (currency_1, currencies_1) in currencies.items():
            for (currency_2, ticker) in currencies_1.items():
                if currency_2 == active or currency_1 == active:
                    continue

                ticker1 = currencies[active][currency_1]
                ticker2 = ticker
                ticker3 = currencies[currency_2][active]

                N = 1 / ticker1 * (1 - COMMISSION)
                M = N / ticker2 * (1 - COMMISSION)
                V = M / ticker3 * (1 - COMMISSION)

                if V > 1:
                    print(V,
                          active,
                          ticker1,
                          currency_1,
                          ticker2,
                          currency_2,
                          ticker3,
                          sep=' ')

    time.sleep(1)
