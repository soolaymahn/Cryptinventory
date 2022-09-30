import csv

if __name__ == '__main__':
    disposition_csv = open("new_dispositions_2021.csv")
    total = 0
    for line in disposition_csv:
        asset, rcv_date, cost_basis, date_sold, proceeds = line.split(",")
        total += float(proceeds) - float(cost_basis)
        total = round(total, 2)
    print(total)
