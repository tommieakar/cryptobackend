import threading

change_mode = False

class MyThread(threading.Thread):

	def __init__(self, func, args):
		threading.Thread.__init__(self)
		self.func = func
		self.args = args
	def run(self):
		self.func(*self.args)

class Variation:

	exchanges_amount = 0
	ticker = {}
	price_spread = {}

def set_exchanges_number(number):
	Variation.exchanges_amount = number

def set_exchanges(exchange):
	Variation.ticker[exchange] = {}
	Variation.price_spread[exchange] = {}

def update_ticker(exchange, ticker):
	Variation.ticker[exchange] = ticker
	for key, value in Variation.ticker.items():
		if key == exchange:
			continue
		if value == {}:
			continue
		price_spread = {}
		price_spread['first'] = key + ' ' + str(value['last_price'])
		price_spread['second'] = exchange + ' ' + str(ticker['last_price'])
		price_spread['ts'] = ticker['ts']
		price_spread['symbol'] = ticker['symbol']
		price_spread['spread'] = float(ticker['last_price']) - float(value['last_price'])
		Variation.price_spread[key] = price_spread
