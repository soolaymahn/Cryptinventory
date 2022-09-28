import csv

if __name__ == '__main__':
    disposition_csv = open("output/new_dispositions_2021.csv")
    total = 0
    for line in disposition_csv:
        asset, rcv_date, cost_basis, date_sold, proceeds, amount = line.split(",")
        total += proceeds - cost_basis
    print(total)
