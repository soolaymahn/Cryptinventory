import csv
import datetime

if __name__ == '__main__':
    avax = open("input/avax", "r")
    output_lines = []
    for line in avax.readlines():
        timestamp, tradeType, amount, currency, size_usd, fee = line.split(',')
        print(timestamp)
        timestamp2 = datetime.datetime.strptime(timestamp, "%m-%d-%YT%H:%M:%S").strftime("%Y-%m-%dT%H:%M:%S")
        if tradeType == 'Buy':
            output_lines.append([timestamp2, tradeType, amount, currency, size_usd, 'USD', '0.54', 'USD', 'AVAX', 'US'])
        elif tradeType == 'Sell':
            output_lines.append([timestamp2, tradeType, size_usd, 'USD', amount, currency, '0.54', 'USD', 'AVAX', 'US'])

    with open('avax-trades.csv', mode='w') as output:
        output = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for txn in output_lines:
            output.writerow(txn)