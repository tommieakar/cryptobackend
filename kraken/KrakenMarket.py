#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
sys.path.append('../MarketApi')

from GlobalVar import *
from restful import *

exchange = 'kraken'
MARKET_URL = "https://api.kraken.com"
headers = {}

previous_price = 0

def get_symbols():
	url = MARKET_URL + '/0/public/AssetPairs'
	rev = eval(http_get_request(url, headers))
	symbols = []
	for symbol in rev['result'].keys():
		symbols.append(symbol)
	return symbols

def get_ticker_merged(symbol, mode):
	try:
		params = {'pair': symbol}
		url = MARKET_URL + '/0/public/Ticker'
		rev = eval(http_get_request(url, headers, params))	
		result = rev['result'][symbol]
		dt, ms = time_transfer(get_time())
		ask = [result['a'][0], result['a'][2]]
		bid = [result['b'][0], result['b'][2]]
		volume = result['v'][0]
		turnover = float(volume) * float(result['p'][0])
		if mode:
			global previous_price
			if previous_price == last_price:
				return {"failmessage": "price no change"}
			else:
				previous_price = last_price
		ticker = {'ts': dt, 'nsec': ms , 'symbol': symbol, 'bid': bid, 'ask': ask, 'last_price': result['c'][0], 'volume':volume, 'turnover':turnover}	
		return ticker
	except Exception as e:
		return {"failmessage": e}       

def print_ticker(symbol):
	while True:
		ticker = get_ticker_merged(symbol, change_mode)
		if ticker.has_key('failmessage'):
			continue
		ticker_str = ticker['ts'] + '\t' + ticker['nsec'] + '\t' + symbol + '\t' + 'bid:' + str(ticker['bid']) + '\t' + 'ask:' + str(ticker['ask']) + '\t'  + 'last_price:' + ticker['last_price']
		print ticker_str

def send_client(symbol, socket):
	while True:
		ticker = get_ticker_merged(symbol, change_mode)
		if ticker.has_key('failmessage'):
			continue
		send_str = 'Full' + '|' + exchange + '|' + symbol + '|' + str(ticker['bid'][0]) + '|' + str(ticker['bid'][1]) + '|' + str(ticker['ask'][0]) + '|' + str(ticker['ask'][1]) + '|' + str(ticker['last_price']) + '|' + str(ticker['volume']) + '|' + str(ticker['turnover']) + '|' +  ' ' + '|' + ticker['ts'] + '|' + ticker['nsec'] + '|' + 'allen' + '|' + 'end'
		socket.send(send_str)
		#print 'server send' + '\t' + send_str

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
#	print get_ticker_merged('XXBTZUSD', False)
	print_ticker('XXBTZUSD')
#	send_client('XXBTZUSD', ' ')
