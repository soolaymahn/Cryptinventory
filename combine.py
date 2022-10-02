import csv

if __name__ == '__main__':
    new_txn_cb = open("output/new.csv", "r")
    new_txn_avx = open("output/avax-trades.csv", "r")
    new_txn_eth = open("output/eth-trades.csv", "r")
    new_txn_celo = open("output/celo-trades.csv", "r")
    new_txn_ply = open("output/new.csv", "r")

    output = new_txn_cb.readlines() + new_txn_avx.readlines() + new_txn_eth.readlines()

    output = sorted(output, key=lambda x: x.split(',')[0])

    with open('all-new.csv', mode='w') as output_file:
        for txn in output:
            output_file.write(txn)
