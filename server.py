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
	
	port = '40021'

	context = zmq.Context()
	socket = context.socket(zmq.PUB)
	socket.bind("tcp://*:%s" %  port)
        hwm = 0
        socket.setsockopt(zmq.HWM, hwm)
        buf_size = 1000000000
        socket.setsockopt(zmq.RCVBUF, buf_size)

	huobi_products = ['btcusdt', 'ethusdt', 'ethbtc', 'xrpbtc', 'ltcusdt', 'ltcbtc', 'etcusdt', 'etcbtc', 'eosusdt', 'eosbtc', 'bchusdt', 'bchbtc', 'trxusdt', 'trxbtc', 'trxeth', 'neousdt', 'neobtc', 'xlmbtc', 'adabtc', 'iotabtc', 'zecbtc', 'qtumbtc', 'dashbtc', 'omgbtc']
	kraken_products = ['XXBTZUSD', 'XETHZUSD', 'XETHXXBT', 'XXRPXXBT', 'XLTCZUSD', 'XLTCXXBT', 'XETCZUSD', 'XETCXXBT', 'XETCXETH', 'EOSUSD', 'EOSXBT', 'BCHUSD', 'BCHXBT', 'XXLMXXBT', 'XZECXXBT']
	okcoin_products = ['btc_usd', 'eth_usd']
	binance_products = ['BTCUSDT', 'ETHUSDT', 'ETHBTC', 'XRPBTC', 'LTCUSDT', 'LTCBTC', 'ETCUSDT', 'ETCBTC', 'ETCETH', 'EOSUSDT', 'EOSBTC', 'BCCUSDT', 'BCCBTC', 'TRXUSDT', 'TRXBTC', 'TRXETH', 'NEOUSDT', 'NEOBTC', 'XLMBTC', 'ADABTC', 'IOTABTC', 'ZECBTC', 'QTUMBTC']
	gdax_products = ['BTC-USD', 'ETH-USD', 'ETH-BTC', 'LTC-USD', 'LTC-BTC', 'ETC-USD', 'ETC-BTC', 'BCH-USD', 'BCH-BTC']
	okex_products = ['btc_usdt', 'eth_usdt', 'eth_btc', 'xrp_btc', 'ltc_usdt', 'ltc_btc', 'etc_usdt', 'etc_btc', 'etc_eth', 'eos_usdt', 'eos_btc', 'bch_usdt', 'bch_btc', 'trx_usdt', 'trx_btc', 'trx_eth', 'neo_usdt', 'neo_btc', 'xlm_btc', 'ada_btc', 'iota_btc', 'zec_btc', 'qtum_btc', 'dash_btc', 'omg_btc']
	poloniex_products = ['USDT_BTC', 'USDT_ETH', 'BTC_ETH', 'BTC_XRP', 'USDT_LTC', 'BTC_LTC', 'USDT_ETC', 'BTC_ETC', 'ETH_ETC', 'USDT_EOS', 'BTC_EOS', 'USDT_BCH', 'BTC_BCH', 'BTC_ZEC', 'BTC_DASH', 'BTC_OMG']

	for product in huobi_products:
		huobi = GlobalVar.MyThread(HuobiMarket.send_client, ('%s' % product, socket))
		huobi.start()
	for product in kraken_products:
		kraken = GlobalVar.MyThread(KrakenMarket.send_client, ('%s' % product, socket))
		kraken.start()
	for product in okcoin_products:
		okcoin = GlobalVar.MyThread(OKcoinMarket.send_client, ('%s' % product, socket))
		okcoin.start()
	for product in binance_products:
		binance = GlobalVar.MyThread(BinanceMarket.send_client, ('%s' % product, socket))
		binance.start()
	for product in gdax_products:
		gdax = GlobalVar.MyThread(GdaxMarket.send_client, ('%s' % product, socket))
		gdax.start()
	for product in okex_products:
		okex = GlobalVar.MyThread(OkexMarket.send_client, ('%s' % product, socket))
		okex.start()
	for product in poloniex_products:
		poloniex = GlobalVar.MyThread(PoloniexMarket.send_client, ('%s' % product, socket))
		poloniex.start()
