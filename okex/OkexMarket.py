#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
sys.path.append('../MarketApi')

from GlobalVar import *
from restful import *

exchange = 'okex'

MARKET_URL = "https://www.okex.com/api/v1"
headers = {
        'Content-Type': 'application/x-www-form-urlenconded',
        }

previous_price = 0

'''
	symbols:
'''

def get_ticker_merged(symbol, mode):
	try:
		params = {'symbol': symbol}
		url_ticker = MARKET_URL + '/ticker.do'
		url_depth = MARKET_URL + '/depth.do'
		rev = eval(http_get_request(url_ticker, headers, params))
		depth = eval(http_get_request(url_depth, headers, params))
		dt, ms = time_transfer(get_time())
		ticker = {'ts': dt, 'nsec': ms , 'symbol': symbol, 'bid': depth['bids'][0], 'ask': depth['asks'][-1], 'last_price': rev['ticker']['last'], 'volume': rev['ticker']['vol'], 'turnover': 0}	
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
		ticker_str = ticker['ts'] + '\t' + ticker['nsec'] + '\t'  + symbol + '\t' + 'bid:' + str(ticker['bid']) + '\t' + 'ask:' + str(ticker['ask']) + '\t' + 'last_price:' + str(ticker['last_price'])
		print ticker_str 

def send_client(symbol, socket):
	while True:
		ticker = get_ticker_merged(symbol, change_mode)
		if ticker.has_key('failmessage'):
			continue
		send_str = 'Full' + '|' + exchange + '|' + symbol + '|' + str(ticker['bid'][0]) + '|' + str(ticker['bid'][1]) + '|' + str(ticker['ask'][0]) + '|' + str(ticker['ask'][1]) + '|' + str(ticker['last_price']) + '|' + str(ticker['volume']) + '|' + str(ticker['turnover']) + '|' +  ' ' + '|' + ticker['ts'] + '|' + ticker['nsec'] + '|' + 'limit' + '|' + 'end'
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
	print_ticker('xrp_btc')
#	send_client('btc_usdt', '')
