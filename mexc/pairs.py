import argparse
import requests

parser = argparse.ArgumentParser(description='MEXC tickers')
parser.add_argument('-f', '--futures', action='store_true')
parser.add_argument('-q', '--quote-asset')

if __name__ == "__main__":
    args = parser.parse_args()
    
    if args.futures:
        symbols = filter(lambda x: x['state'] ==  0, requests.get('https://contract.mexc.com/api/v1/contract/detail').json()['data'])
        symbols = map(lambda x: 'MEXC:{}.P'.format(x['symbol'].replace('_', '')), symbols)
        print(',\n'.join(sorted(symbols)))
    else:
        symbols = filter(lambda x: x['status'] == 'ENABLED', requests.get('https://api.mexc.com/api/v3/exchangeInfo').json()['symbols'])
        if args.quote_asset:
            symbols = filter(lambda x: x['quoteAsset'] == args.quote_asset, symbols)
        symbols = map(lambda x: 'MEXC:{}'.format(x['symbol']), symbols)
        print(',\n'.join(sorted(symbols)))