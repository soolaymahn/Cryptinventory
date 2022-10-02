import datetime
import csv

if __name__ == '__main__':
    polygon = open("input/polygon-in", "r")
    output_lines = []
    for line in polygon.readlines():
        type, timestamp, out_amount, out_currency, in_amount, in_currency, size_usd = line.split(',')
        timestamp2 = datetime.datetime.strptime(timestamp, "%b-%d-%Y %I:%M:%S %p +UTC").strftime("%Y-%m-%dT%H:%M:%S")
        output_lines.append([timestamp2, 'Sell', float(size_usd), 'USD', float(out_amount), out_currency, '0', 'USD', 'POLYGON', 'US'])
        output_lines.append([timestamp2, 'Buy', float(in_amount), in_currency, float(size_usd), 'USD', '0', 'USD', 'POLYGON', 'US'])

    with open('output/poly-trades.csv', mode='w') as output:
        output = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for txn in output_lines:
            output.writerow(txn)