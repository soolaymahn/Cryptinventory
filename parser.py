import csv

if __name__ == '__main__':
    pro = open("input/pro.csv", "r")
    # retail = open("retail.csv", "r")
    with open('output/cb-pro.csv', mode='w') as output:
        output = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # for line in retail.readlines():
        #     if len(line.split(",")) > 9:
        #         print(line)
        #     timestamp, tradeType, asset, quantity, spotPrice, subtotal, total, fee, notes = line.split(",")
        #
        #     fee_currency = "USD"
        #     exchange = "Coinbase"
        #     if tradeType == 'Buy':
        #         in_amount = quantity
        #         out_amount = subtotal
        #         in_currency = asset
        #         out_currency = 'USD'
        #
        #     if tradeType == 'Sell':
        #         in_amount = subtotal
        #         out_amount = quantity
        #         in_currency = 'USD'
        #         out_currency = asset
        #
        #     if tradeType == 'Convert':
        #         note_items = notes.split(' ')
        #         out_amount = note_items[1]
        #         out_currency = note_items[2]
        #         in_amount = note_items[4]
        #         in_currency = note_items[5]
        #         tradeType = 'Trade'
        #
        #     if tradeType == 'Send':
        #         out_currency = asset
        #         out_amount = quantity
        #         in_amount = ''
        #         in_currency = ''
        #         fee = ''
        #         fee_currency = ''
        #         exchange = ''
        #
        #     if tradeType == 'Receive':
        #         out_currency = ''
        #         out_amount = ''
        #         in_amount = quantity
        #         in_currency = asset
        #         fee = ''
        #         fee_currency = ''
        #         exchange = ''
        #
        #     if tradeType == 'Rewards Income':
        #         in_amount = quantity
        #         in_currency = asset
        #         fee = ''
        #         fee_currency = ''
        #         exchange = ''
        #         out_currency = ''
        #         out_amount = ''
        #         tradeType = 'staking'
        #
        #     if tradeType == 'Coinbase Earn':
        #         tradeType = 'misc reward'
        #         in_amount = quantity
        #         in_currency = asset
        #         fee = ''
        #         fee_currency = ''
        #         exchange = ''
        #         out_currency = ''
        #         out_amount = ''
        #
        #     if tradeType in {'misc reward'}:
        #         output.writerow(
        #             [timestamp, tradeType, in_amount, in_currency, out_amount, out_currency, fee, fee_currency,
        #              exchange,
        #              'Yes'])
        #     pass
        for line in pro.readlines():
            portfolio, trade_id, product, side, timestamp, size, size_unit, price, fee, total, total_unit = line.split(
                ",")
            # TODO: properly handle trades
            if product == 'REP-BTC':
                tradeType = 'Trade'
                in_currency = 'REP'
                in_amount = size
                out_currency = 'BTC'
                out_amount = abs(float(total)) - float(fee)
                fee_currency = 'BTC'
            if product == 'WBTC-BTC':
                btc_price = 47770.58
                usd_total = abs(float(total)) * btc_price
                usd_fee = abs(float(fee)) * btc_price
                output.writerow(
                    [timestamp, 'Sell', usd_total, 'USD', abs(float(total)), 'BTC', fee, 'USD',
                     'Coinbase Pro',
                     'Yes'])
                output.writerow(
                    [timestamp, 'Buy', size, 'WBTC', usd_total, 'USD', fee, 'USD',
                     'Coinbase Pro',
                     'Yes'])
                continue
            if product == 'MATIC-BTC':
                btc_price = 35000.58
                usd_total = abs(float(total)) * btc_price
                usd_fee = abs(float(fee)) * btc_price
                output.writerow(
                    [timestamp, 'Sell', usd_total, 'USD', abs(float(total)), 'BTC', fee, 'USD',
                     'Coinbase Pro',
                     'Yes'])
                output.writerow(
                    [timestamp, 'Buy', size, 'MATIC', usd_total, 'USD', fee, 'USD',
                     'Coinbase Pro',
                     'Yes'])
                continue
            else:
                product_items = product.split('-')
                fee_currency = 'USD'
                if side == 'BUY':
                    in_currency = product_items[0]
                    in_amount = size
                    out_currency = 'USD'
                    out_amount = abs(float(total)) - float(fee)
                    tradeType = 'Buy'
                if side == 'SELL':
                    in_currency = 'USD'
                    in_amount = abs(float(total)) - float(fee)
                    out_currency = product_items[0]
                    out_amount = size
                    tradeType = 'Sell'
            if in_currency == 'CGLD':
                in_currency = 'CELO'
            if out_currency == 'CGLD':
                out_currency = 'CELO'
            output.writerow(
                [timestamp, tradeType, in_amount, in_currency, out_amount, out_currency, fee, fee_currency,
                 'Coinbase Pro',
                 'Yes'])
