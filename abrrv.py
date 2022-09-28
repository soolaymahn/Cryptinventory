import csv

if __name__ == '__main__':
    pro_csv = open("output/pro.csv", "r")
    output = []
    for line in pro_csv.readlines():
        timestamp, tradeType, in_amount, in_currency, out_amount, out_currency, \
        fee, fee_currency, ex, us = line.split(",")
        if len(output) > 0:
            timestamp2, tradeType2, in_amount2, in_currency2, out_amount2, out_currency2, \
            fee2, fee_currency2, ex2, us2 = output[-1]
            if timestamp2 == timestamp and tradeType2 == tradeType:
                output.pop()
                output.append([timestamp, tradeType, float(in_amount) + float(in_amount2), in_currency,
                               float(out_amount) + float(out_amount2), out_currency, float(fee) + float(fee2),
                               fee_currency, ex, "Yes"])
                continue

        output.append([timestamp, tradeType, float(in_amount), in_currency,
                       float(out_amount), out_currency, float(fee),
                       fee_currency, ex, "Yes"])

    with open('output/output-abrv.csv', mode='w') as output_file:
        output_file = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for line in output:
            output_file.writerow(line)
