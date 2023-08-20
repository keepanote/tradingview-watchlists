import argparse
import requests

parser = argparse.ArgumentParser(description='Gateio tickers')
parser.add_argument('-m', '--margin', action='store_true')
parser.add_argument('-f', '--futures', action='store_true')
parser.add_argument('-q', '--quote-asset')

if __name__ == "__main__":
    args = parser.parse_args()

    if args.futures:
        symbols = filter(lambda x: x['in_delisting'] == False, requests.get('https://api.gateio.ws/api/v4/futures/usdt/contracts').json())
        symbols = map(lambda x: 'GATEIO:{}.P'.format(x['name'].replace('_', '')), symbols)
        print(',\n'.join(sorted(symbols)))
    else:
        symbols = filter(lambda x: x['trade_status'] == 'tradable', requests.get('https://api.gateio.ws/api/v4/spot/currency_pairs').json())
        # if args.margin:
        #     # 全仓杠杆支持的币种列表
        #     symbols = filter(lambda x: x['status'] == 1, requests.get('https://api.gateio.ws/api/v4/margin/cross/currencies').json())
        if args.quote_asset:
            symbols = filter(lambda x: x['quote'] == args.quote_asset and not ("3S" in x['base'] or "5S" in x['base'] or "3L" in x['base'] or "5L" in x['base']), symbols)
        symbols = map(lambda x: 'GATEIO:{}'.format(x['id'].replace('_', '')), symbols)
        print(',\n'.join(sorted(symbols)))
