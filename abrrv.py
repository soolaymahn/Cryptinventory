import csv

if __name__ == '__main__':
    pro_csv = open("output/pro.csv", "r")
    output = []
    map = {}
    for line in pro_csv.readlines():
        timestamp, tradeType, in_amount, in_currency, out_amount, out_currency, \
        fee, fee_currency, ex, us = line.split(",")

        if timestamp in map and tradeType in map[timestamp]:
            map[timestamp][tradeType].append(line)
        elif timestamp in map:
            map[timestamp][tradeType] = [line]
        else:
            map[timestamp] = {tradeType: [line]}

    for timestamp, tradeTypeMap in map.items():
        for tradeType, lines in tradeTypeMap.items():
            total_in = 0
            total_out = 0
            total_fee = 0
            _, _, _, in_currency, _, out_currency, \
            _, fee_currency, ex, us = lines[0].split(",")
            for line in lines:
                timestamp, tradeType, in_amount, in_currency, out_amount, out_currency, \
                fee, fee_currency, ex, us = line.split(",")
                total_in += float(in_amount)
                total_out += float(out_amount)
                total_fee += float(fee)
            output.append([timestamp, tradeType, total_in, in_currency,
                           total_out, out_currency, total_fee,
                           fee_currency, ex, "Yes"])

    output = sorted(output, key=lambda x: x[0])
    with open('output/new.csv', mode='w') as output_file:
        output_file = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for line in output:
            output_file.writerow(line)
