import time
import requests

TIMEOUT = 100

MARKET_URL = ""

headers = {}

def get_time():
        t = time.time()
        timestamp = int(round(t * 1000))
        return timestamp

def time_transfer(timestamp):
        ms = str(timestamp%1000)
        timestamp = timestamp/1000
        time_local = time.localtime(timestamp)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
       	dt = dt[11:]
        ms = ms.zfill(3)
        return dt, ms

def http_get_request(url, headers, params={}, add_to_headers=None):
        if add_to_headers:
                headers.update(add_to_headers)
        try:
                res = requests.get(url, params=params, headers=headers, timeout=TIMEOUT)
                if res.status_code == 200:
                        return res.text
        except Exception as e:
                return {"failmessage": e}

