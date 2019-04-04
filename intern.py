import zmq
import sys
sys.path.append('./MarketApi')
sys.path.append('./huobi')
sys.path.append('./kraken')
sys.path.append('./okcoin')
sys.path.append('./binance')
sys.path.append('./gdax')
sys.path.append('./okex')
sys.path.append('./poloniex')

import GlobalVar
import HuobiMarket
import KrakenMarket
import OKcoinMarket
import BinanceMarket
import GdaxMarket
import OkexMarket
import PoloniexMarket

if __name__ == '__main__':
	
	port = '4002'

	context = zmq.Context()
	socket = context.socket(zmq.PUB)
	socket.bind("tcp://*:%s" %  port)
        hwm = 0
        socket.setsockopt(zmq.HWM, hwm)
        buf_size = 1000000000
        socket.setsockopt(zmq.RCVBUF, buf_size)

	huobi_products = ['btcusdt', 'ethusdt', 'ethbtc', 'xrpbtc', 'ltcusdt', 'ltcbtc', 'etcusdt', 'etcbtc', 'eosusdt', 'eosbtc', 'bchusdt', 'bchbtc', 'trxusdt', 'trxbtc', 'trxeth', 'neousdt', 'neobtc', 'xlmbtc', 'adabtc', 'iotabtc', 'zecbtc', 'qtumbtc', 'dashbtc', 'omgbtc']
	okex_products = ['btc_usdt', 'eth_usdt', 'eth_btc', 'xrp_btc', 'ltc_usdt', 'ltc_btc', 'etc_usdt', 'etc_btc', 'etc_eth', 'eos_usdt', 'eos_btc', 'bch_usdt', 'bch_btc', 'trx_usdt', 'trx_btc', 'trx_eth', 'neo_usdt', 'neo_btc', 'xlm_btc', 'ada_btc', 'iota_btc', 'zec_btc', 'qtum_btc', 'dash_btc', 'omg_btc']
	binance_products = ['BTCUSDT', 'ETHUSDT', 'ETHBTC', 'XRPBTC', 'LTCUSDT', 'LTCBTC', 'ETCUSDT', 'ETCBTC', 'ETCETH', 'EOSUSDT', 'EOSBTC', 'BCCUSDT', 'BCCBTC', 'TRXUSDT', 'TRXBTC', 'TRXETH', 'NEOUSDT', 'NEOBTC', 'XLMBTC', 'ADABTC', 'IOTABTC', 'ZECBTC', 'QTUMBTC']

	for product in binance_products:
		binance = GlobalVar.MyThread(BinanceMarket.send_client, ('%s' % product, socket))
		binance.start()
