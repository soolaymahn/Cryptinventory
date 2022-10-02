import csv
import datetime

if __name__ == '__main__':
    eth = open("input/eth-in", "r")
    output_lines = []
    for line in eth.readlines():
        print(line)
        timestamp, tradeType, amount, currency, size_usd, fee = line.split(',')
        timestamp2 = datetime.datetime.strptime(timestamp, "%m-%d-%YT%H:%M:%S").strftime("%Y-%m-%dT%H:%M:%S")
        if tradeType == 'Buy':
            output_lines.append([timestamp2, tradeType, amount, currency, size_usd, 'USD', float(fee), 'USD', 'ETH', 'US'])
        elif tradeType == 'Sell':
            output_lines.append([timestamp2, tradeType, size_usd, 'USD', amount, currency, float(fee), 'USD', 'ETH', 'US'])

    with open('eth-trades.csv', mode='w') as output:
        output = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for txn in output_lines:
            output.writerow(txn)