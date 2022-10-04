import datetime
import csv

import requests


def convert_date(date):
    date = date.replace('May', '05')
    date = date.replace('April', '04')
    date = date.replace(' +-4 UTC', '')
    return datetime.datetime.strptime(date, "%m-%d-%Y %I:%M:%S %p")


class TradeRow(object):
    def __init__(self, date, trade_type, in_amount, in_currency, out_amount, out_currency):
        dt = convert_date(date)
        dt += datetime.timedelta(hours=4)
        self.dt = dt
        self.timestamp = dt.strftime("%Y-%m-%dT%H:%M:%S%z")
        self.trade_type = trade_type
        self.in_amount = in_amount
        self.in_currency = in_currency
        self.out_amount = out_amount
        self.out_currency = out_currency

    def to_row(self):
        return [self.timestamp, self.trade_type, self.in_amount, self.in_currency, self.out_amount, self.out_currency,
                '0', 'USD', 'Celo', 'US']


class RewardRow(object):
    def __init__(self, timestamp, in_amount, in_currency, usd_value):
        dt = convert_date(timestamp)
        dt += datetime.timedelta(hours=-3)
        self.date = dt.strftime("%m/%d/%Y")
        self.in_amount = str(float(in_amount))
        self.in_currency = in_currency
        self.usd_value = round(usd_value, 2)

    def to_row(self):
        return [self.date, self.in_amount + " " + self.in_currency, self.usd_value]


def parse_prices():
    prices_map = {}
    price_csv = open("input/celo-prices.csv")
    for line in price_csv:
        symbol, date, price = line.split(',')
        prices_map[symbol + date] = float(price)
    return prices_map


def parse_swaps(prices_map):
    swaps_csv = open("input/ube-swaps")
    swaps = []
    for line in swaps_csv:
        date, asset1, asset2 = line.rstrip('\n').split(',')
        asset1_amount, asset1_symbol = asset1.split(' ')
        asset2_amount, asset2_symbol = asset2.split(' ')
        asset1_symbol = asset1_symbol.upper()
        asset2_symbol = asset2_symbol.upper()
        usd_value = get_usd_value(asset1_amount, asset1_symbol, asset2_amount, asset2_symbol, prices_map, date)
        trade1 = TradeRow(date, 'Sell', usd_value, 'USD', asset1_amount, asset1_symbol)
        trade2 = TradeRow(date, 'Buy', asset2_amount, asset2_symbol, usd_value, 'USD')
        swaps.append(trade1)
        swaps.append(trade2)
    return swaps


def get_usd_value(asset1_amount, asset1_symbol, asset2_amount, asset2_symbol, prices_map, date):
    if is_stable(asset1_symbol):
        return asset1_amount
    if is_stable(asset2_symbol):
        return asset2_amount
    if is_euro(asset1_symbol):
        return float(asset1_amount) * 1.2
    if is_euro(asset2_symbol):
        return float(asset2_amount) * 1.2
    month, day = date.split("-2021")[0].split("-")
    if month == 'May':
        month = "05"
    elif month == 'April':
        month = "04"
    elif month == '5':
        month = "05"

    if 'PM' in date:
        day = str(int(day) + 1)
        if int(day) < 10:
            day = '0' + day
    if asset2_symbol == 'CELO' or asset1_symbol not in ['CELO', 'UBE']:
        return prices_map[asset2_symbol + month + '-' + day] * float(asset2_amount)
    return prices_map[asset1_symbol + month + '-' + day] * float(asset1_amount)


def is_stable(symbol):
    if symbol == 'CUSD' or symbol == 'MCUSD':
        return True
    return False


def is_euro(symbol):
    if symbol == 'CEUR' or symbol == 'MCEUR':
        return True
    return False


def parse_liquidity(prices_map):
    liquidity_csv = open("input/ube-liquidity")
    liquids = []
    for line in liquidity_csv:
        if line == '\n':
            continue
        direction, date, asset_1, asset_2, ulp = line.rstrip('\n').split(',')
        asset1_amount, asset1_symbol = asset_1.strip().split(' ')
        asset2_amount, asset2_symbol = asset_2.strip().split(' ')
        ulp_amount, _ = ulp.split(' ')
        asset1_symbol = asset1_symbol.upper()
        asset2_symbol = asset2_symbol.upper()
        sorted_syms = sorted([asset1_symbol, asset2_symbol])
        usd_value = float(get_usd_value(asset1_amount, asset1_symbol, asset2_amount, asset2_symbol, prices_map, date))

        if direction == '+':
            trade1 = TradeRow(date, 'Sell', usd_value, 'USD', asset1_amount, asset1_symbol)
            trade2 = TradeRow(date, 'Sell', usd_value, 'USD', asset2_amount, asset2_symbol)
            trade3 = TradeRow(date, 'Buy', ulp_amount, "ULP" + "-" + sorted_syms[0] + "-" + sorted_syms[1],
                              usd_value * 2,
                              'USD')
        else:
            trade1 = TradeRow(date, 'Buy', asset1_amount, asset1_symbol, usd_value, 'USD')
            trade2 = TradeRow(date, 'Buy', asset2_amount, asset2_symbol, usd_value, 'USD')
            trade3 = TradeRow(date, 'Sell', usd_value * 2, 'USD', ulp_amount,
                              "ULP" + "-" + sorted_syms[0] + "-" + sorted_syms[1])

        liquids.append(trade1)
        liquids.append(trade2)
        liquids.append(trade3)
    return liquids


def parse_rewards(prices_map):
    rewards_csv = open("input/ube-rewards", "r")
    rewards = []
    reward_buys = []
    for line in rewards_csv.readlines():
        date, reward = line.split(',')
        reward_usd = get_usd_value(reward, 'UBE', 0, '', prices_map, date)
        # TODO: update bought at zero
        trade = TradeRow(date, 'Buy', float(reward), 'UBE', 0, 'USD')
        reward = RewardRow(date, reward, 'UBE', reward_usd)
        rewards.append(reward)
        reward_buys.append(trade)
    return rewards, reward_buys


if __name__ == '__main__':
    pm = parse_prices()
    rewards, reward_buys = parse_rewards(pm)
    txns = parse_liquidity(pm) + parse_swaps(pm) + reward_buys
    # with open('celo-rewards.csv', mode='w') as output:
    #     output = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     for reward in rewards:
    #         total += float(reward.in_amount)
    #         output.writerow(reward.to_row())
    txns = sorted(txns, key=lambda x: x.dt)
    with open('output/celo-trades.csv', mode='w') as output:
        output = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for txn in txns:
            output.writerow(txn.to_row())
