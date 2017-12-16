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


def create_dictionary(pairs):
    order_book = polo.returnOrderBook(depth=1)
    dictionary = collections.defaultdict(dict)

    for pair in pairs:
        p = pair.upper()
        src, dst = split(p)

        ask_order = order_book[p]['asks'][0]
        src_ask = {
            'pair': src + '_' + dst,
            'price': float(ask_order[0]),
            'amount': float(ask_order[1])
        }

        bid_order = order_book[p]['bids'][0]
        src_bid = {
            'pair': dst + '_' + src,
            'price': 1 / float(bid_order[0]),
            'amount': float(bid_order[1]) * float(bid_order[0])
        }

        dictionary[src][dst] = src_ask
        dictionary[dst][src] = src_bid

    return dictionary


def get_amount():
    amount_3 = order_3['amount'] * order_3['price']

    amount_2 = order_2['amount'] if order_2['amount'] < amount_3 else amount_3
    amount_2 = amount_2 * order_2['price']

    return order_1['amount'] if order_1['amount'] < amount_2 else amount_2


while True:
    polo = Poloniex()
    pairs = coin_pairs()
    orders = create_dictionary(pairs)

    print('Waiting...')

    for active in MAIN_ACTIVE:
        for (currency_1, currencies_1) in orders.items():
            for (currency_2, order) in currencies_1.items():
                if currency_2 == active or currency_1 == active:
                    continue

                order_1 = orders[active][currency_1]
                order_2 = order
                order_3 = orders[currency_2][active]

                # Формируем объем
                # TODO проверка баланса
                amount = get_amount()
                order_price = order_1['price'] * amount

                transfer_1 = amount * (1 - COMMISSION)
                transfer_2 = transfer_1 / order_2['price'] * (1 - COMMISSION)
                transfer_3 = transfer_2 / order_3['price'] * (1 - COMMISSION)

                if (transfer_3 / order_price) > 1:
                    print('##############')
                    print('Find percent:', transfer_3)
                    print('Amount:', str(amount), currency_1)
                    print('Order price:', str(order_price), active)
                    print('Income:', str(transfer_3), active)
                    print('Orders:')
                    print(order_1, '=>')
                    print(order_2, '=>')
                    print(order_3)

    time.sleep(1)
