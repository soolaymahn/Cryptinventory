import csv

if __name__ == '__main__':
    avax = open("input/avax", "r")
    output_lines = []
    for line in avax.readlines():
        timestamp, tradeType, in_amount, in_currency, out_amount, fee = line.split(',')
        output_lines.append([timestamp, tradeType, in_amount, in_currency, out_amount, 'USD', '0.54', 'USD', 'AVAX', 'US'])

    with open('avax-trades.csv', mode='w') as output:
        output = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for txn in output_lines:
            output.writerow(txn)