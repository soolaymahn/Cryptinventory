import csv

if __name__ == '__main__':
    disposition_csv = open("output/new_dispositions_2021.csv")
    total = 0
    for line in disposition_csv:
        asset, rcv_date, cost_basis, date_sold, proceeds = line.split(",")
        total += float(proceeds) - float(cost_basis)
        total = round(total, 2)
    print(total)
    # disposition_csv = open("output/all-new.csv")
    # celo_total = 0
    # for line in disposition_csv:
    #     timestamp, tradeType, in_amount, in_currency, out_amount, out_currency, fee, fee_currency, ex, us = line.split(",")
    #     if tradeType == 'Buy' and in_currency == 'CELO' and ex == 'Coinbase Pro':
    #         celo_total += float(out_amount)
    #
    # print(celo_total)
