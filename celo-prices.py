import requests
import csv


def build_prices():
    with open('output2.csv', mode='w') as output:
        output = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # for x in range(20, 30):
        #     resp = requests.get('https://api.coingecko.com/api/v3/coins/celo/history?date=' + str(x) + '-04-2021')
        #     output.writerow(['CELO', '04-' + str(x), resp.json()['market_data']['current_price']['usd']])
        # for x in range(1, 25):
        #     str_x = str(x)
        #     if x < 10:
        #         str_x = '0' + str_x
        #     resp = requests.get('https://api.coingecko.com/api/v3/coins/celo/history?date=' + str_x + '-05-2021')
        #     output.writerow(['CELO', '05-' + str_x, resp.json()['market_data']['current_price']['usd']])

        for x in range(7, 25):
            str_x = str(x)
            if x < 10:
                str_x = '0' + str_x
            resp = requests.get('https://api.coingecko.com/api/v3/coins/ubeswap/history?date=' + str_x + '-05-2021')
            output.writerow(['UBE', '05-' + str_x, resp.json()['market_data']['current_price']['usd']])


if __name__ == '__main__':
    build_prices()
