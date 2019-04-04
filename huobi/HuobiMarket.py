#/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
sys.path.append('../MarketApi')

from restful import *
from GlobalVar import *

exchange = 'huobi'
MARKET_URL = "https://api.huobi.pro"
headers = {
        'Content-Type': 'application/x-www-form-urlenconded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
        }

previous_price = 0

def get_symbols():
	url = MARKET_URL + '/v1/common/symbols'
	result = eval(http_get_request(url, headers))
	symbols = []
	for symbol in result['data']:
		symbols.append(symbol['symbol'])
	return symbols

def get_ticker_merged(symbol, mode):
	try:
		params = {'symbol': symbol}
		url = MARKET_URL + '/market/detail/merged'
		rev = eval(http_get_request(url, headers, params))
		dt, ms = time_transfer(get_time())
		ticker = {'ts': dt, 'nsec': ms, 'symbol': symbol, 'bid': rev['tick']['bid'], 'ask': rev['tick']['ask'], 'last_price': rev['tick']['close'], 'volume': rev['tick']['amount'], 'turnover': rev['tick']['vol']}
		if mode:
			global previous_price
			if previous_price == ticker['last_price']:
				return {"failmessage": "price no change"}
			else:
				previous_price = ticker['last_price']
		return ticker 
	except Exception as e:
		return {"failmessage": e}       

def print_ticker(symbol):
	while True:
		ticker = get_ticker_merged(symbol, change_mode)
		if ticker.has_key('failmessage'):
			continue
		ticker_str = ticker['ts'] + '\t' + ticker['nsec']  + '\t' + symbol + '\t' + 'bid:' + str(ticker['bid']) + '\t' + 'ask:' + str(ticker['ask']) + '\t' + 'last_price:' + str(ticker['last_price'])
		print ticker_str 

def send_client(symbol, socket):
	while True:
		ticker = get_ticker_merged(symbol, change_mode)
		if ticker.has_key('failmessage'):
			continue
		send_str = 'Full' + '|' + exchange + '|' + symbol + '|' + str(ticker['bid'][0]) + '|' + str(ticker['bid'][1]) + '|' + str(ticker['ask'][0]) + '|' + str(ticker['ask'][1]) + '|' + str(ticker['last_price']) + '|' + str(ticker['volume']) + '|' + str(ticker['turnover']) + '|' +  ' ' + '|' + ticker['ts'] + '|' + ticker['nsec'] + '|' + 'allen' + '|' + 'end'
		socket.send(send_str)
		#print 'server send' + '\t'  + send_str

def get_merged(symbol):
	while True:
	 	ticker = get_ticker_merged(symbol, change_mode)
		if ticker.has_key('failmessage'):
			continue
		update_ticker(exchange, ticker)
		for key, value in Variation.price_spread.items():
			if value == {}:
				continue
			if key == exchange:
				continue
			print value

if __name__ == '__main__':
	print get_symbols()
#	print_ticker('btcusdt')
#	send_client('btcusdt', '')
