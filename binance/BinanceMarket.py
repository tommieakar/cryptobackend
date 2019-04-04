#/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
sys.path.append('../MarketApi')

from restful import *
from GlobalVar import *

exchange = 'binance'
MARKET_URL = "https://api.binance.com"
headers = {
        'Content-Type': 'application/x-www-form-urlenconded',
        }

previous_price = 0

def get_symbols():
	url = MARKET_URL + '/api/v1/exchangeInfo'
	result = http_get_request(url, headers)
	print result

def get_ticker_merged(symbol, mode):
	try:
		params = {'symbol': symbol}
		url_price = MARKET_URL + '/api/v3/ticker/price'
		url_book = MARKET_URL + '/api/v3/ticker/bookTicker'
		url_24hr = MARKET_URL + '/api/v1/ticker/24hr'
                print url_price
		last_price = eval(http_get_request(url_price, headers, params))
		bookTicker = eval(http_get_request(url_book, headers, params))
		hr = eval(http_get_request(url_24hr, headers, params))
		volume = hr['volume']
		turnover = float(volume) * float(hr['weightedAvgPrice'])
		dt, ms = time_transfer(get_time())
		ticker = {'ts': dt, 'nsec': ms, 'symbol': symbol, 'bid': [bookTicker['bidPrice'], bookTicker['bidQty']], 'ask': [bookTicker['askPrice'], bookTicker['askQty']], 'last_price': last_price['price'], 'volume': volume, 'turnover': turnover}
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
                        print ticker
			continue
		send_str = 'Full' + '|' + exchange + '|' + symbol + '|' + str(ticker['bid'][0]) + '|' + str(ticker['bid'][1]) + '|' + str(ticker['ask'][0]) + '|' + str(ticker['ask'][1]) + '|' + str(ticker['last_price']) + '|' + str(ticker['volume']) + '|' + str(ticker['turnover']) + '|' +  ' ' + '|' + ticker['ts'] + '|' + ticker['nsec'] + '|' + 'allen' + '|' + 'end'
		socket.send(send_str)
		print send_str

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
#	print get_ticker_merged('BTCUSDT', '')
	print_ticker('BTCUSDT')
#	send_client('BTCUSDT', '')
