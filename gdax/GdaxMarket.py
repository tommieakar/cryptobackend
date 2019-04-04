#/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
sys.path.append('../MarketApi')

from restful import *
from GlobalVar import *

exchange = 'gdax'
MARKET_URL = "https://api.prime.coinbase.com"
headers = {}

previous_price = 0

def get_symbols():
	url = MARKET_URL + '/products'
	result = http_get_request(url, headers)
	print result

def get_ticker_merged(symbol, mode):
	try:
		url_book = MARKET_URL + '/products/%s/book' % symbol
		url_ticker = MARKET_URL + '/products/%s/ticker' % symbol
		book = eval(http_get_request(url_book, headers))
		product_ticker = eval(http_get_request(url_ticker, headers))
		dt, ms = time_transfer(get_time())
		ticker = {'ts': dt, 'nsec': ms, 'symbol': symbol, 'bid': [book['bids'][0][0], book['bids'][0][1]], 'ask': [book['asks'][0][0], book['asks'][0][1]], 'last_price': product_ticker['price'], 'volume': product_ticker['volume'], 'turnover': 0}
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
		ticker_str = ticker['ts'] + '\t' + ticker['nsec'] + '\t' + symbol + '\t' + 'bid:' + str(ticker['bid']) + '\t' + 'ask:' + str(ticker['ask']) + '\t' + 'last_price:' + str(ticker['last_price'])
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
#	get_symbols()
	print_ticker('BTC-USD')
#	send_client('BTC-USD', '')
