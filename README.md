# cryptobackend

brief introduction:
This is the backend code for cryptocurrency market_data, included exchanges: huobi, okex, binance, polenix, kakren

how it works with CryptoUI (https://github.com/nickhuangxinyu/CryptoUI)

cryptobackend run in a server, it fetchs marketdata from exchanges, and send it in a fixed port(for now, 42001), then the ui can get
data from the ip:port and show in the ui. Also, the real arb trading program can get it to send trading signal.

see the real data:

download the demo.rar, see the README of https://github.com/nickhuangxinyu/CryptoUI

system:

both windows and linux are fine, since it's a python project.
python2.7
pyzmq install needed, you can use set_pyzmq.sh in this repository.
notice: these exchanges's server address are blocked in china.

run command:

python server.py
it will occupy port 40021 in your computer.

Author:
XinYu Huang

any questions or suggestions are welcome, please contract me with:huangxy17@fudan.edu.cn, i will list your name here to thanks for
your contribution.

Thanks list:
1.Allen Lee(from fudan university)
