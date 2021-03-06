import requests,json
import random
import urllib3
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import threading, queue

# 海外代理
def get(targetUrl):
    # targetUrl = "https://api.ip.sb/geoip"
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    proxyUser = "scnuxiaokun"
    password = "scnuxiaokun123"
    randomId = random.randint(1,99999999)
    proxyUrl = 'proxy.fanqieip.net:12344'
    athorization = proxyUser+"-"+"us"+"-"+str(randomId)+":"+password

    proxy = {"http": "http://" + athorization+"@"+proxyUrl, "https": "http://" + athorization+"@"+proxyUrl}
    headers = {
        # "Proxy-Authorization": 'Basic ' + athorization,
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4"}

    # logger.info(athorization+"@"+proxyUrl)
    timeout = 3
    r = requests.get(url=targetUrl, headers=headers, proxies=proxy, verify=False, allow_redirects=False, timeout=timeout)
    if r.status_code == 302 or r.status_code == 301:
        loc = r.headers['Location']
        url_f = loc
        r = requests.get(url_f, headers=headers, proxies=proxy, verify=False, allow_redirects=False, timeout=timeout)
        return r
    return r

# 海外代理
def postV2(targetUrl, json, headers):
    # targetUrl = "https://api.ip.sb/geoip"
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    proxyUser = "scnuxiaokun"
    password = "scnuxiaokun123"
    randomId = random.randint(1,99999999)
    proxyUrl = 'proxy.fanqieip.net:12344'
    athorization = proxyUser+"-"+"us"+"-"+str(randomId)+":"+password

    proxy = {"http": "http://" + athorization+"@"+proxyUrl, "https": "http://" + athorization+"@"+proxyUrl}

    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0"
    headers["Accept-Language"] = "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4"

    response = requests.post(url=targetUrl, json=json, headers=headers, proxies=proxy, verify=False, allow_redirects=False)
    return response

# 蘑菇代理
# 蘑菇代理
def getV2(targetUrl):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    # 蘑菇代理的隧道订单
    appKey = "UTNOMUx6WE1EQzJrVUU0VDpTd0JDVTFzNk1zY2pybW9q"

    # 蘑菇隧道代理服务器地址
    ip_port = 'secondtransfer.moguproxy.com:9001'

    proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}
    headers = {
        "Proxy-Authorization": 'Basic ' + appKey,
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4"}

    timeout = 3
    r = requests.get(url=targetUrl, headers=headers, proxies=proxy, verify=False, allow_redirects=False,timeout=timeout)
    if r.status_code == 302 or r.status_code == 301:
        loc = r.headers['Location']
        url_f = loc
        r = requests.get(url_f, headers=headers, proxies=proxy, verify=False, allow_redirects=False, timeout=timeout)
        return r
    return r
# 蘑菇代理
# 无认证代理
def getV3(targetUrl):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    # 蘑菇代理的隧道订单
    appKey = "U3NJT2hUMUN3OTVrRklVZTpwandpTVY5T1hKczlqYUUx"

    # 蘑菇隧道代理服务器地址
    ip_port = 'http-pro.moguproxy.com:9003'

    proxy = {"http": "http://" + ip_port}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4"}

    # timeout = 10
    r = requests.get(url=targetUrl, headers=headers, proxies=proxy, verify=False, allow_redirects=False)
    if r.status_code == 302 or r.status_code == 301:
        loc = r.headers['Location']
        url_f = loc
        r = requests.get(url_f, headers=headers, proxies=proxy, verify=False, allow_redirects=False)
        return r
    return r

# 蘑菇代理，传入代理IP
def getV4(targetUrl, ip_port):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4"}

    timeout = 10
    r = requests.get(targetUrl, headers=headers, proxies=proxy, timeout=timeout, verify=False, allow_redirects=False)
    if r.status_code == 302 or r.status_code == 301:
        loc = r.headers['Location']
        url_f = loc
        r = requests.get(url_f, headers=headers, proxies=proxy, timeout=timeout, verify=False, allow_redirects=False)
        return r
    return r

#获取代理ip
def getIpPort(ipPortQueue):
    if ipPortQueue.qsize() > 2:
        return ipPortQueue.get()

    executor = ThreadPoolExecutor(max_workers=1)
    executor.submit(fetchIpPortToQueue, ipPortQueue)

    if ipPortQueue.qsize() > 0:
        return ipPortQueue.get()
    return None

#获取蘑菇私密API代理
def fetchIpPortToQueue(ipPortQueue):
    try:
        fo = open("proxy.config")
        url = fo.read()
        fo.close()
        response = requests.get(url)
        print(response.status_code)
        print(response.text)
        map = json.loads(response.text)
        for item in map['msg']:
            ipPortQueue.put(item['ip'] + ":" + item['port'])
    except BaseException as Argument:
        print("Exception:" + str(Argument))
    else:
        pass

# 蘑菇隧道代理
# 无认证代理
def post(targetUrl, json, headers):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    # 蘑菇代理的隧道订单
    # appKey = "U3NJT2hUMUN3OTVrRklVZTpwandpTVY5T1hKczlqYUUx"

    # 蘑菇隧道代理服务器地址
    ip_port = 'http-pro.moguproxy.com:9003'

    proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}
    # headers["Proxy-Authorization"] = 'Basic ' + appKey
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0"
    headers["Accept-Language"] = "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4"

    response = requests.post(url=targetUrl, json=json, headers=headers, proxies=proxy, verify=False, allow_redirects=False)
    return response

def postByIpPort(targetUrl, json, headers, ipPort):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    proxy = {"http": "http://" + ipPort, "https": "https://" + ipPort}
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0"
    headers["Accept-Language"] = "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4"
    timeout = 10
    response = requests.post(url=targetUrl, json=json, headers=headers, proxies=proxy, verify=False,
                             allow_redirects=False, timeout=timeout)
    return response


# if __name__ == '__main__':
#     ipPortQueue = queue.SimpleQueue()
#     fetchIpPortToQueue(ipPortQueue)