import argparse
import requests
# https://www.okx.com/docs-v5/zh/
parser = argparse.ArgumentParser(description='Okx tickers')
# SPOT：币币
# FUTURES：交割合约
# SWAP：永续合约
# OPTION：期权
parser.add_argument('-m', '--margin', action='store_true')
parser.add_argument('-f', '--futures', action='store_true')
parser.add_argument('-s', '--swap', action='store_true')
parser.add_argument('-o', '--option', action='store_true')
parser.add_argument('-q', '--quote-asset')

if __name__ == "__main__":
    args = parser.parse_args()
    baseUrl = 'https://www.okx.com/api/v5/public/instruments?instType='

    if args.margin: 
        symbols = requests.get(baseUrl +'MARGIN').json()['data']
        symbols = map(lambda x: 'OKX:{}'.format(x['instId'].replace('-', '')), symbols)
        print(',\n'.join(sorted(symbols)))
    if args.futures: 
        symbols = requests.get(baseUrl +'FUTURES').json()['data']
        symbols = map(lambda x: 'OKX:{}'.format(x['instId'].replace('-', '')), symbols)
        print(',\n'.join(sorted(symbols)))
    if args.swap: # SWAP：永续合约
        symbols = requests.get(baseUrl +'SWAP').json()['data']
        symbols = map(lambda x: 'OKX:{}'.format(x['instId'].replace('-', '')), symbols)
        print(',\n'.join(sorted(symbols)))
    # if args.option: # OPTION：期权
    #     symbols = requests.get(baseUrl +'OPTION').json()['data']
    #     symbols = map(lambda x: 'OKX:{}'.format(x['instId'].replace('-', '')), symbols)
    #     print(',\n'.join(sorted(symbols)))
    
    if not args.margin and not args.futures and not args.swap and not args.option: # SPOT：币币
        symbols = requests.get(baseUrl +'SPOT').json()['data']
        if args.quote_asset:
            # 使用列表推导式格式化instId字段
            symbols = filter(lambda x: x.get('quoteCcy') == args.quote_asset, symbols)
        # 并去除前缀"OKX:"后存在的-
        symbols = map(lambda x: 'OKX:{}'.format(x['instId'].replace('-', '')), symbols)
        print(',\n'.join(sorted(symbols)))
