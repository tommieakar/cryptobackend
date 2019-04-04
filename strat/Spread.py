#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
sys.path.append('../huobi')
sys.path.append('../kraken')
sys.path.append('../okcoin')

import GlobalVar
import HuobiMarket
import KrakenMarket
import OKcoinMarket

if __name__ == '__main__':
	GlobalVar.set_exchanges_number(2)
	GlobalVar.set_exchanges('huobi')
	GlobalVar.set_exchanges('kraken')
	GlobalVar.set_exchanges('okcoin')

	huobi = GlobalVar.MyThread(HuobiMarket.get_merged, ('btcusdt', ))
	kraken = GlobalVar.MyThread(KrakenMarket.get_merged, ('XXBTZUSD', ))
	okcoin = GlobalVar.MyThread(OKcoinMarket.get_merged, ('btc_usd',))
	huobi.start()
	kraken.start()
	okcoin.start()
