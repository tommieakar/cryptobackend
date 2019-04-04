#!/bin/bash
sudo yum install -y uuid uuid-devel libuuid libuuid-devel
cd ~
wget https://files.pythonhosted.org/packages/52/e4/23f54fd3e81abfa228ee6278a5a2b099e17e2023ed841bd415d070b5ea94/pyzmq-static-2.1.4.tar.gz
pip install pyzmq-static-2.1.4.tar.gz
