import datetime


class TradeRow(object):
    def __init__(self, line):
        self.timestamp, self.tradeType, self.in_amount, self.in_currency, self.out_amount, self.out_currency, \
        self.fee, self.fee_currency, self.ex, self.us = line.split(",")
        if self.in_amount != "":
            self.in_amount = float(self.in_amount)
        if self.out_amount != "":
            self.out_amount = float(self.out_amount)
        if self.tradeType == 'Sell':
            self.in_amount = self.in_amount - float(self.fee)
        elif self.tradeType == 'Buy':
            self.out_amount = self.out_amount + float(self.fee)
        if len(self.in_currency) > 0 and self.in_currency[0] == '"':
            self.in_currency = self.in_currency[1:-1]
        self.is2021 = False
        if self.ex == 'Coinbase Pro':
            if self.timestamp.startswith('2021'):
                self.is2021 = True
            self.timestamp = datetime.datetime.strptime(self.timestamp, "%Y-%m-%dT%H:%M:%S.%f%z").timestamp()
        else:
            self.timestamp = datetime.datetime.strptime(self.timestamp, "%Y-%m-%dT%H:%M:%S%z").timestamp()


class DispositionRow(object):
    def __init__(self, line):
        self.asset, self.rcv_date, self.cost_basis, self.date_sold, self.proceeds = line.split(",")
        self.rcv_date = datetime.datetime.strptime(self.rcv_date, "%m/%d/%Y").timestamp()
        self.date_sold = datetime.datetime.strptime(self.date_sold, "%m/%d/%Y").timestamp()


class DispositionRow2(object):
    def __init__(self, asset, rcv_dat, cost_basis, data_sold, proceeds, amount):
        self.asset = asset
        self.rcv_date = rcv_dat
        self.cost_basis = cost_basis
        self.date_sold = data_sold
        self.proceeds = proceeds
        self.amount = amount


def parse_old():
    return parse_old_sells(parse_old_buys())


def parse_old_buys():
    old_txn_csv = open("old_transactions.csv", "r")
    asset_map = {}
    for line in old_txn_csv.readlines():
        row = TradeRow(line)
        if row.is2021:
            continue
        if row.in_currency not in asset_map:
            asset_map[row.in_currency] = [row]
        else:
            asset_map[row.in_currency].append(row)
    return asset_map


def parse_new_tx():
    # TODO: combine all sources
    new_txn_csv = open("new_transactions.csv", "r")
    asset_map = {}
    for line in new_txn_csv.readlines():
        row = TradeRow(line)
        if row.tradeType == 'Sell':
            map_currency = row.out_currency
        else:
            map_currency = row.in_currency
        if map_currency not in asset_map:
            asset_map[map_currency] = [row]
        else:
            asset_map[map_currency].append(row)
    for asset in asset_map.keys():
        asset_map[asset].sort(key=lambda x: x.timestamp)
    return asset_map


def sort_dispositions(dsp):
    # earliest to latest date
    return sorted(dsp, key=lambda x: x.rcv_date)


def parse_old_sells(old_inventory):
    old_dsp_csv = open("old_dispositions.csv", "r")
    dsp_map = {}
    for line in old_dsp_csv.readlines():
        row = DispositionRow(line)
        if row.asset not in dsp_map:
            dsp_map[row.asset] = [row]
        else:
            dsp_map[row.asset].append(row)

    sorted_dsp = {asset: sort_dispositions(dispositions) for asset, dispositions in dsp_map.items()}

    old_dsp2, old_inventory2 = optimistic_cancel(old_inventory, sorted_dsp)
    return old_inventory2
    # return fifo_cancel(old_inventory2, old_dsp2)


def optimistic_cancel(old_inventory, old_dsp):
    old_dsp2 = {}
    old_inventory2 = {}
    for asset, dispositions in old_dsp.items():
        latest_dsp = dispositions[-1].rcv_date
        old_inventory2[asset] = list(filter(lambda x: x.timestamp > latest_dsp, old_inventory[asset]))
        old_dsp2[asset] = list(filter(lambda x: x.rcv_date == latest_dsp, dispositions))
    return old_dsp2, old_inventory2


def fifo_cancel(old_inventory, old_dsp):
    old_inventory2 = {}
    for asset, dispositions in old_dsp.items():
        asset_inv = list(filter(lambda x: x.tradeType == 'Buy', old_inventory[asset]))
        for disposition in dispositions:
            dsp_basis = disposition.cost_basis
            while dsp_basis > 0:
                asset_buy = asset_inv[0]
                if dsp_basis < asset_buy.out_amount:
                    # Update other fields
                    asset_buy.out_amount = asset_buy.out_amount - dsp_basis
                    dsp_basis = 0
                else:
                    dsp_basis = dsp_basis - asset_buy.out_amount
                    asset_inv.pop(0)
        # TODO?: merge non-buys
        old_inventory2[asset] = asset_inv

    return old_inventory2


def highest_basis_cancel(inventory):
    # parse old to heap
    # cancel sell inline
    # new txn must include on-chain

    new_txns = parse_new_tx()
    new_dispositions = {}

    for asset, txns in new_txns.items():
        if asset not in ['CRV']: # For Testing
            continue
        for row in txns:
            if row.tradeType == 'Buy':
                if row.in_currency not in inventory:
                    inventory[row.in_currency] = [row]
                else:
                    inventory[row.in_currency].append(row)
            elif row.tradeType == 'Sell':
                # (stretch): long term cap gains optimization
                inventory[row.out_currency].sort(key=lambda x: x.out_amount/x.in_amount, reverse=True)
                out_amount = row.out_amount
                while out_amount > 0:
                    if len(inventory[row.out_currency]) == 0 and out_amount < 0.000001:
                        out_amount = 0
                        continue
                    asset_buy = inventory[row.out_currency][0]
                    if out_amount < asset_buy.in_amount:
                        cost_basis = asset_buy.out_amount * (out_amount / asset_buy.in_amount)
                        new_dsp = DispositionRow2(asset=row.out_currency, rcv_dat=asset_buy.timestamp,
                                                  cost_basis=cost_basis,
                                                  data_sold=row.timestamp, proceeds=row.in_amount, amount=out_amount)
                        asset_buy.in_amount = asset_buy.in_amount - out_amount
                        asset_buy.out_amount = asset_buy.out_amount - cost_basis
                        out_amount = 0
                    else:
                        inventory[row.out_currency].pop(0)
                        proceeds = row.in_amount * (asset_buy.in_amount / out_amount)
                        new_dsp = DispositionRow2(asset=row.out_currency, rcv_dat=asset_buy.timestamp,
                                                  cost_basis=asset_buy.out_amount,
                                                  data_sold=row.timestamp,
                                                  proceeds=proceeds,
                                                  amount=asset_buy.in_amount)
                        row.in_amount = row.in_amount - proceeds
                        out_amount = out_amount - asset_buy.in_amount
                    if row.out_currency in new_dispositions:
                        new_dispositions[row.out_currency].append(new_dsp)
                    else:
                        new_dispositions[row.out_currency] = [new_dsp]

    return inventory, new_dispositions


if __name__ == '__main__':
    inventory, new_dispositions = highest_basis_cancel(parse_old())
