# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import requests,json
import _thread,threading
import urllib3
import logging
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import threading, queue

# 创建Logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 创建Handler

# 终端Handler
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)

# 文件Handler
fileHandler = logging.FileHandler('log.log', mode='w', encoding='UTF-8')
fileHandler.setLevel(logging.NOTSET)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
consoleHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)

# 添加到Logger中
logger.addHandler(consoleHandler)
logger.addHandler(fileHandler)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

def getByProxy(targetUrl):
    # 蘑菇代理的隧道订单
    appKey = "dlpwN1prQWpNdUpIazVOcjplclFxRVVuOFZyYXdHRXhC"

    # 蘑菇隧道代理服务器地址
    ip_port = 'secondtransfer.moguproxy.com:9001'

    proxy = {"http": "http://" + ip_port}
    headers = {
        "Proxy-Authorization": 'Basic ' + appKey,
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4"}

    r = requests.get(url=targetUrl, headers=headers, proxies=proxy, verify=False, allow_redirects=False)
    if r.status_code == 302 or r.status_code == 301:
        loc = r.headers['Location']
        url_f = loc
        r = requests.get(url_f, headers=headers, proxies=proxy, verify=False, allow_redirects=False)
        return r
    return r

def postByProxy(targetUrl, json, headers):
    # 蘑菇代理的隧道订单
    appKey = "eEJlb2Z5c09BVEVQNWpCbzpjWGJ3T1ZES01VdzZ6OWZV"

    # 蘑菇隧道代理服务器地址
    ip_port = 'secondtransfer.moguproxy.com:9001'

    proxy = {"http": "http://" + ip_port}
    headers["Proxy-Authorization"] = 'Basic ' + appKey
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0"
    headers["Accept-Language"] = "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4"

    logger.info(headers)
    response = requests.post(url=targetUrl, json=json, headers=headers, proxies=proxy, verify=False, allow_redirects=False)
    logger.info(response.status_code)
    logger.info(response.text)


def getInventory(url):
    # logger.info("请求URL:"+url)
    # response = requests.get(url=url)
    response = getByProxy(url)
    if response.status_code == 200:
        return json.loads(response.text).get('inventory')
    else:
        logger.error("[ERROR]:"+" status_code:"+ str(response.status_code)+ " "+url)  # 打印状态码
        return -1

def autoBuyProductByCode(productCode):
    url = 'http://www.ti.com.cn/storeservices/cart/opninventory?opn=' + productCode + "&abc=123"
    logger.info("[" + productCode + "]" + "查库存")
    inventory = getInventory(url)
    if inventory > 0:
        logger.info("["+productCode+"]" + "库存数量:" + str(inventory))
    elif inventory == 0:
        logger.info("[" + productCode + "]" + "没库存")
    else:
        logger.info("[" + productCode + "]" + "查询失败")

def getProductList(productCodeQueue, size):
    if productCodeQueue.qsize() < size:
        f = open("data.txt")
        lines = f.readlines()
        f.close()
        for index in range(len(lines)):
            line = lines[index]
            productCode = line.replace('\n', '').replace('\r', '').strip()
            productCodeQueue.put(productCode)

    list = []
    for index in range(size):
        if productCodeQueue.empty() == False:
            list.append(productCodeQueue.get())
        else:
            return list
    return list

def loopProductListToGetInventory():

    maxThreadCount = 10
    maxIpCount = 5
    executor = ThreadPoolExecutor(max_workers=maxThreadCount)
    all_task = []
    productCodeQueue = queue.SimpleQueue()

    while 1:
        productCodeList = getProductList(productCodeQueue, 5)
        tasks = [executor.submit(autoBuyProductByCode, (item)) for item in productCodeList]
        for task in tasks:
            all_task.append(task)

        time.sleep(1)

        if len(all_task) >= maxThreadCount :
            copy_all_task = all_task

            for future in as_completed(copy_all_task):
                all_task.remove(future)
                if len(all_task) <= maxThreadCount - maxIpCount:
                    break

    logger.info("===========全部完成===========")

def addtocart(productCode):
    addtocart_url = "https://www.ti.com.cn/occservices/v2/ti/addtocart"
    click_url = "https://www.ti.com.cn/AmOjk0fvT/J8j/8V0/oI2Ez1rk_18I/3ftOkGQShi/FUc-Ej0B/EA8Q/IBQPZhcB"

    # session = requests.Session()
    # cookies = "ti_ua=Mozilla%2f5.0%20(Macintosh%3b%20Intel%20Mac%20OS%20X%2010_15_6)%20AppleWebKit%2f537.36%20(KHTML,%20like%20Gecko)%20Chrome%2f93.0.4577.82%20Safari%2f537.36; user_pref_language=\"zh-CN\"; CONSENTMGR=ts:1632830176853%7Cconsent:true; tiSessionID=017c2c433e580045588fc3c4eb1403078002607000bd0; _ga=GA1.3.1733809788.1632830178; _gid=GA1.3.510459219.1632830178; _gcl_au=1.1.1688808738.1632830178; ELOQUA=GUID=443D61824E09450D9A104DFC43A5D3DA; __adroll_fpc=3a7669f09c2d2e7abd89dcdb22696713-1632830265312; login-check=null; login-check=null; user_pref_shipTo=\"CN\"; user_pref_currency=\"CNY\"; ti_bm=; user_pref_givenNameLocalLanguage=\"%E8%94%A1\"; bm_sz=D8501E7A1B46748538392CE1C475D2A7~YAAQPg1x30/kvQZ8AQAACOXJMQ3Mb+Z2zf3Xsm58trr2/CI6/WX6EhiS1iKdKMdcTfbLxS9j3g76Sf/ivm7RUcIFhse1DtvZyEqZNY8GSdJDSV8QkcyiSk+1medee3bhie9w5rcVBtDBKQISixFMHOkoxykRt0+F8dSxWLw7ge1hTCOSxqVufQQtnW3zI8LbunfhX0+BkLRzwvS22hBHEuUmX0oavQJTRDn8TKGF0Z4PohmXjbn8kwff/blWRSmIgOFIcRQbBauZtKCGU9ZtCIbLI+6RR6Iuf2r9Pmi5zZkUzQ==~3159600~3551283; bm_mi=928CE7FB8A15DDB213E09F9F26619659~i3fL8BRGvMOY/GkZMz6Xz/AE6WUH51fSKuLexWjwQHmmcftPQQ4ED8szXnRCpB5ANIp0aa9Mh7KOP8R9/d2onKWnVMdK9nE0fsuN/S+yKTM3068UzEw9uCeodawT6QyE+2wPkFEueSLXcF+2psOSelNgv/GkQuhxy0keN7cA274f9T6q44/KAsbd7/tPt4tPo43ABDU1AHSMMbtLeMwfaCyQIkHTsO+6iOPrvQhBm+BhCsVzWP26JfKIAw0X+LIFFxDY+xaCU/OjZ2wdmGfjUxIS+W34MERpZd0BJXg48TU+JFKCB/kpFT9O+yoJq5pz; acceleratorSecureGUID=4b19c0594a27d48fbfab3f5ae0f57d333ef488a4; user_pref_permanentId=\"6822002\"; user_pref_uid=\"scnu_xiaokun@qq.com\"; last-domain=www.ti.com.cn; ti_geo=country=CN|city=SHANGHAI|continent=AS|tc_ip=61.173.26.177; __ar_v4=4PSIDGQM4FBWJL6XJJ2EQC%3A20210929%3A6%7CFJT6BT4YWNEOROP3BJ7ITA%3A20210929%3A5%7CIEC2AV647FHDNBUGU23SN7%3A20210929%3A5%7CQFXRHQEHOJDMLHSLFIWCLO%3A20210928%3A3%7C2XNKMR6P4VGD5MD3ZP4SQR%3A20210928%3A3%7CG3YHLXUICZC3XKDXYVVLO4%3A20210928%3A3%7CS4HGNHQ7DNGNJDUXJ2XJA3%3A20210928%3A5%7C3GLIROW56VGDFM2KUHWC42%3A20210928%3A5%7CDMF3YWNTG5HTZP5WNBOFAA%3A20210928%3A5; auth_session=C6-X-MJdqqcHKoZ5.7pknfap9Cc577TZMQm_lTpzAphy4SOmANxeQT02TCXZVV6-T2sjNkTMmUK5Q9SrBn1l7oiLPszKcEF_GVJ_BCxh-ry9opSSucsl3x4D6lO-8up_6sqg_9zipkHM8_rN9a5dAVOhIyeVNcRjAuS22_FhQpQAIiRey_9ZdlRbBXRMOiy_AbWBohQTN6ONvTfURrlVb74fgNB7DZASjseezmZBB5runPFuGDpU887OAOFHl5RmpJ7_7e9XdFCYlo09mVfMRpCPjcPLNgQjuTco_Q7vpll1wwUm0woVYQgCiCEyg29dc1QaqVQ0zjHMCa-YxiuuX_cNKpNblhfxQ0_Cd0vvZe2ZxPXim5UBPOWePnMeQOt4rs-EpeN3hF_p07FSu6DLI8iDXQxcfwKPet4lgBRY2LCtLyNqke_wXt-MAu2D3dV5NG5s9AYSkSzBzTd2ZfMR640jEMtJpXzv-Pki09RB5VsK3vmyDuW-lKBmHh0_WTNw4F2dEl7jaTU_zTYH-8AYFHfDxfVYGtXsXZXrveofRpGMs7yyyoHtVXXCv5Prty_m4D7DdVjqphvKey5fSUEaWEe5BoIe7qF3EUTaUbu9wPg0cUCEmcUDGRT9eFh1WjAWVLl1vEFBlyEv0o4RnZGA97FWoz7Gq4_UGl_fLbPZG7psftCcA3M8xYKHE9csDIcGxOEH-9z3R-8296n9VY1sa3Mt-3icIRWaiQrTJ01UYPlSqhpFUSYIdTm38-4nbMcvMlT5koKZMHl48XR9sSmEDWY9JDrKdZgA-jsHEOpZiEEY1w8-_-5ZQlicxx7-RxS-H4HLizDDE3QQNXL8DzYpmwKQjt754QFwWfPeiwC8jNY78t6vc8B7yWZKaXmy4aj33ZPAB03ArlqF7t0HDc5LnX8zlZD9ebwZ7jD5jbEw9MYIGusidUIbu20aOKWPw4o6AtCwMc_qSWV-CVJpOricra2ecLQpbC-ky_n9cNB80a07rSaez8zxNZaj3pDalR47wFQzCDMEVkmo8yxoz4UL6NGvQAdX6H0MEiATnuLyt35yYzngeSyj0KpvgnRXdbpj3B9ipwCOEk6y6k_UXSj_gHqdDY3LWebbD9nG_J555Pgwff4ejRd7ykEsMQM3HD_ZoXP4ywBnCxdJl0btevsnqOif2UOAYuCySd9KlJlhLcCTj-rxMCB9_4W0_8uj-RTJ2e2yGlL6_uh91A3FIvmQnm8N0Bcd6L7d9THJZ62rtoT1jl8Te0rIN8gm-DWeQmp87mOG_aXBCXB1p_MYm0gZGnJ43Q-053WIJkovqdsahXvrfP_nr5wgLNtVAzRGF9Qjh6i3T7HJob79VUHEUbfOtYFh40tFa-UMAwSZybXFGpVlx1sjXGl7UsrMWC-z9DxUdDFnXPKhkvdGm7hDk28mVySEnZJ4Zk4HpVRl8tHuitK1YkFh-ih4tNRQOlC-Wv0nGV4QyN71bud34T_iRFR5geWORizzndxIFUtCRAATXBvgjG92G722MidX48mkxrib_gCCxDsu-927tAv-umEfXrk2cOfKSlyIBbJLTZ6pfp5qvfT1vAtR_1DJVoztX4i-7PRDOG4yuRf612d5dIsViCt8rSer2ombvHH8J3UUuWSXENqNBmEwEqutcymLx0T-v6cN9L7QQdeZHjdZSOUBJ3wDnmDl7mEjRrPYa8hdREWx7sgpFgzM0qskYxiT_3bAZdUZwnH_uaFCpoP58DzFOGlALvwyCFusRoHj6iq93PWcVv_VgYr1H88v7HXlretXP-sL_a1gEa2D92gsNwsjsAo_PPShww-PovMjzBk0bylhWUDtO-sSYRTjlpitzmxY8xVh958ItEkhNUmbn-w0hwiqtuX_lItekEANqF2QZuS52FS6a4YxFfh_8MbQm6U652WLs9ILOYeSw7k2J4IZBIQr4Q-aUYPwpj403etxBeJK9q3NlExzWTOKFMMQNwpuaWDnMz7UweUAZcxsrfJboj9GNiJQ8LMggis3cVe2HUu1x_m1itn9Sp7afxWJo9urlFeNcx8-nfs-Z5a3FpGajmq2mkGuC_XI0Bij9OAZyJ09lNcBjUwFYa-w5dwFOBFg2oi6xsUNhaIVfvVWKC5MzUmqrhZU-Rknv8eNTvP5JAJGA6LuXTrIrOVH11DruHLPo8ITOh0_mCW5xCBSN4mI.unzOiXnBezJ-yQgCqBU-5w; gpn=AWR2243-gpn; tipage=%2Fanalog%20%26%20mixed-signal%2Fsensors%2Fmmwave%20radar%20sensors%2Fautomotive%20mmwave%20radar%20sensors%2Fawr2243%2Fproduct%20folder-awr2243-cn; tipageshort=product%20folder-awr2243-cn; ticontent=%2Fanalog%20%26%20mixed-signal%2Fsensors%2Fmmwave%20radar%20sensors%2Fautomotive%20mmwave%20radar%20sensors%2Fawr2243; ga_page_cookie=product%20folder-awr2243-cn; ga_content_cookie=%2Fanalog%20%26%20mixed-signal%2Fsensors%2Fmmwave%20radar%20sensors%2Fautomotive%20mmwave%20radar%20sensors%2Fawr2243; ABTasty=uid=j6wshax2z59xfgv8&fst=1632830177486&pst=1632907900612&cst=1632922936733&ns=3&pvt=33&pvis=10&th=686831.851794.15.8.2.1.1632830480571.1632924246395.1_759046.943435.6.6.1.1.1632907981896.1632924253873.1; ABTastySession=mrasn=&sen=22&lp=https%253A%252F%252Fwww.ti.com.cn%252F; utag_main=v_id:017c2c433e580045588fc3c4eb1403078002607000bd0$_sn:3$_ss:0$_st:1632926058056$free_trial:false$_pn:11%3Bexp-session$ses_id:1632922935894%3Bexp-session; da_sid=5C752F108E33AE88501EAA134867B2BF9C|4|0|3; da_lid=6F461C239A72EA2BDA16BB990A787153DA|0|0|0; da_intState=; user_pref_givenName=\"%E8%94%A1\"; _abck=D98E4E551CDCA02D2A26334F85012BB5~0~YAAQNgnnc6mywsJ7AQAAfvbeMQbklJ48WZN0ZLuM8JcUxo1ZfeaQ6U/tDwghIHWZAEEMwPEtMBHVYe++ACYbEboi6YjjMBNVc/eHzFCvIYhGU84DQ7uZLlIrNSzRWzIQ+PRWF0+wDQPwwYs5nJLOqOcfZp7Qkvk/LtHICsHAUIibpGZgxz4Yfis/+JHRdegLVXjweGo2nsO31sxjQjbOhS6YIp6OrAZ3DCj+NVo/vhy134pGootLXRFzPvnNFLu8V2SCsbjXPgP5jdHIxoyJW0bKdaKCWw/zKHFEtoWSsuZlhxvNz5SqUKMqK4xtkRlP5qkWCpuWc1a/aSrE0w+AL35d7UDwqr8upJ+n/nQwBOin9x2PZ67qGv5z4BKSI+x18S/0VaIlcgrsmfEAzCB9jdPTrcJqkOGwq4wtbwXqRkiwpetiqX0+fXkEuLU=~-1~-1~-1; ak_bmsc=40B762430E202876EB3B47530EBC90A5~000000000000000000000000000000~YAAQNgnnc37gwsJ7AQAAiJ7hMQ1HBWbhadcy+TBZBSdodLu3e9afrDJ7PtYkxACw6dcop5NOy0iwMUMUHEk6NXlRGdgvFQIhIgsyNr53qmZbTpSt8D8hbx741M5d7dRsvKdzweMaG1i3xo6NUN2UylcLThimIrTbgOoh5boPS5oeqdL/MhL25HAZ242awlBtbdGHVh+9i6P6I/ZeqgLOY6e5GYVzTubCyZfs3AibyVqmO3eD1wc+KCTwkIBHjd4CyQGSS2btsR5dUu/WcO87RufNohHroCdY8otNXYCOjZaNsuwcbxLiDFmJ5z/ahC3D61X7kuqWdQT5iKzUPLY+rhvyG8WvHfJM/B+OC3qzLHyTrcCkaitalwrcIGTqmlEWtFsCJOZaQiWbBc57fVaq47EGEqao5DvgHPlfDLQglKQJWyjEe7W+EESk7CIyjcN2o5bW7tbbwlfpvicYNR/LSc6riSyIa9wxcednDv7IzsTumIv3oOWkYA+i1Z/xTEdJNVAopQNn; bm_sv=5461BAE77D732C4B2D138FCD81100F1F~8HY+i93S1dallYFMy749jK4eVyXXWkGKHp44a+0DBW/+TM4yMnpT2/cpdJtyajmm4ZZwftFvlYdsycu4CopRLuICp5WcvM9yo+YnWRu9ph73k8kZZWv00q7bGLmwsE47dZ8Zs5O3XQSOEhJ+MPJTukw+NGlph7uZ2y2d9d1dLEg=; ti_rid=8c65aff2"
    # cookies2 = dict(map(lambda x:x.split('='),cookies.split(";")))
    # for k, v in cookies2.items():
    #     session.cookies[k] = v
    # print(cookies2)

    # 添加请求头，需要就传
    header = {
        "Host": 'www.ti.com.cn',
        "Connection": 'keep-alive',
        "Content-Length": '203',
        "Pragma": 'no-cache',
        "Cache-Control": 'no-store, must-revalidate',
        "sec-ch-ua": '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        "sec-ch-ua-mobile": '?0',
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
        "Content-Type": 'application/json',
        "X-Sec-Clge-Req-Type": 'ajax',
        "Expires": '0',
        "sec-ch-ua-platform": '"macOS"',
        "Accept": '*/*',
        "Origin": 'https://www.ti.com.cn',
        "Sec-Fetch-Site": 'same-origin',
        "Sec-Fetch-Mode": 'cors',
        "Sec-Fetch-Dest": 'empty',
        "Referer": 'https://www.ti.com.cn/store/ti/zh/p/product/?p=TAS5558DCA',
        "Accept-Encoding": 'gzip, deflate, br',
        "Accept-Language": 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'Cookie': 'user_pref_language="zh-CN"; CONSENTMGR=ts:1632830176853%7Cconsent:true; tiSessionID=017c2c433e580045588fc3c4eb1403078002607000bd0; _ga=GA1.3.1733809788.1632830178; _gcl_au=1.1.1688808738.1632830178; ELOQUA=GUID=443D61824E09450D9A104DFC43A5D3DA; __adroll_fpc=3a7669f09c2d2e7abd89dcdb22696713-1632830265312; user_pref_shipTo="CN"; user_pref_currency="CNY"; ti_ua=Mozilla%2f5.0%20(Macintosh%3b%20Intel%20Mac%20OS%20X%2010_15_6)%20AppleWebKit%2f537.36%20(KHTML,%20like%20Gecko)%20Chrome%2f94.0.4606.61%20Safari%2f537.36; ti_bm=; login-check=null; login-check=null; _fbp=fb.2.1633072810262.713331343; _gid=GA1.3.556612117.1633701966; coveo_visitorId=b56afeff-9650-45c5-949f-d6472c282a7f; user_pref_givenNameLocalLanguage="%E8%94%A1"; __ar_v4=4PSIDGQM4FBWJL6XJJ2EQC%3A20210929%3A6%7CFJT6BT4YWNEOROP3BJ7ITA%3A20210929%3A5%7CIEC2AV647FHDNBUGU23SN7%3A20210929%3A5%7CQFXRHQEHOJDMLHSLFIWCLO%3A20210928%3A7%7C2XNKMR6P4VGD5MD3ZP4SQR%3A20210928%3A7%7CG3YHLXUICZC3XKDXYVVLO4%3A20210928%3A7%7CS4HGNHQ7DNGNJDUXJ2XJA3%3A20210928%3A5%7C3GLIROW56VGDFM2KUHWC42%3A20210928%3A5%7CDMF3YWNTG5HTZP5WNBOFAA%3A20210928%3A5; acceleratorSecureGUID=30efc0b0932fcff5ef734ae774e6eca9df1e71a4; auth_session=s6z4fQOLzENQjfnm.cAvqUCK97eTLg6ywNHuKZWn_tyP8-E_DKkdw9Lic7n2MsyLnfX-WNyHGcFyxIzjOEUYUDltjGpSwWN_XFNKiQISkv0CFaxti8hR4GgvLLPPKbOHgZ_bEx2y36XUbg_ep2F-ltfjgicG4kMxNma3UiEOu3osiQ9W79wnVirT0jIYoJ9Gsb4J93WX4KqUBUS5KlHSKP0esPt-xJhBfWUtpo1RWnrnBS_QEqhuxBExIwMunAPt5PQm-Z-O6-1fxRbPDEwRBnjcdvkTNXujmsouAfKI8heL04t00NE9AkcokEzYwJ4SnzBeOxgCDJrPFSYof86GN5aIgFe9U9sVUgK7XvKwUSEN8iPieSDAeqA9MMwe4ZtU82e7EixoCg7n7yHivNwgX5WjJ8FU-kS0OOPueo9be5bIcGCVfLHwSws17gn6im987jw5yNaC2nzZnU_uBE7Ogcm9fo46ZBALXIqnfH3I9D-q4HNqctbLMjyyBJgaHPz8-a7t0c8MGdfTU49QKHN6A59a6LZapZq-fpQIEWdvwYEZLz0t7FtlNmyy4G8xFeFbjkMcUyVp6SyD6RJ0767gVZfGKZBUswdscmttXs-5lewqQGDOAAtCwlvOiAEup0JPWPD6-kXCY9taGX7oMwJssPs1SGHPneGxlV4ZYkpiX9l2iRJypY3NY154QlqOY7t30oqms5DYe_xiIdD4m2gdurUagmFArOP2m1jDqNmdQCUck-igJjpP_tdLXNFdjR47_ZpQDXeih_epJZLmlizI1fsrUSPaMUWqNVnhbcDgsG8fOBGf2cGbhx5964eaHmaGIw0cJEgOkzer8CTNWtlyzRt87unNd1t75E1HkkYM1PgEIWELtcq4lmbeJkdIUdOaYI0PhS2BjHfhtPGIH0HHQDgCzqcYtXSipImzWXVLtWfVRt9nNyRsgi9ZueGBX4Ggr9Gha8uzYSYpJCu9GruIsscESjl-FRFr1DXF0JlYNFeyF9NWRYsMglXkrR1iFYJmEp1Cz2WEiEaoJhog3KY_0QPJhjLxwwNbtStm_zSy78LE7v_DGNYEcseMSTbzkNjugl941Ru4eHCPZWJU5_k8bkM1If33N0-2CFS629DiW8VpAS-EGN54U2A1hW2iVJTAnGmv24mM7oNWzUiwGSMl3pqcnnlMah6-bFcMjVI6FBYWZMeZJbsfgohu5diax1VbEwlUuFvzvCwyHkhdMuRhoDn8vgqH6E3ochHjtbtE3-Vt02UB1ZS0ZDUGE2RD_hidGsdlHdg3KALItajoQwN3wLA1K5RgosDWaBa0dJi4LK5y72wvozdYmB6_Kd-Q5BD3o9KzPC9ehtLmblCxRxU6NlVOzB_HihlRT9K0VESnh3MqeqBjvW6EyK55PTOeLvoCDQRKQpHTRaPU-7vTnLc5IQ2iGcqdrjMitBKiO4wsqhPo2Fuoqf5qfB8sLSUBw0Ssb5Uf5wQCxqyFTPac2K6vzudBVLZq5Cc1u-VTSw1etqfhuhYIlBu-HLSxleoylOKvhs49tfXoAjM1uNn1IzbOBdshtUX-PNeYROcdo3offrjKVZ4Km_beKxr0xiZxm72m1g-SSSer8TQ1GFyoUQ6-uhbzG27zvd9-xcRQiNEQpkpM4RPdrR9vgG-_GdSYSjHMNbCpSCseJuPQsVlXl81dCi1pFjAoQX1vwM2NsdYsoR-GO2ht8r3iQLASc37C6Ffavfex6d8zXP1-F20O2y4N7KFM.8Bl_L1mM7bMLU9AysiPA_Q; ti_get_lit=ts%3D1633773225982%7Clit%3Ddrv8353%7Cpid%3D%7Caid%3D%7Cgpn%3DNon-Product%7Cpt%3Dsearch%7Cevt%3D202199175345982%7C; ti_geo=country=CN|city=SHANGHAI|continent=AS|tc_ip=210.13.100.178; user_pref_permanentId="6822002"; user_pref_uid="scnu_xiaokun@qq.com"; bm_sz=B35EC6A38F8EA0193377C12F602D6937~YAAQtgrgeolRjVV8AQAAG5myaA3jDOIzK2+PqoAgjO71p4QJra3JW2M5DM5RyWUchZUGmcfMDfRw9sDrFBe/gRTfMG++0orDkWIcGEDDKKogxHOwuddXskt8g2yFYMxFYjnYB69O6b46cUp4EzNsGYcEEXkvv5vn5FALwEouT7boKvVSmxbqN9ENTkleXRYrp3CJrIeTMlFnI0GdvRGY/9CkPytAmSFaz81TYgikCcq2V5204nQcUFXiuv5HSNcMYOZgy178w05bnd1uG1V8u4mHqOeI4zPAIjsIVj02xFSdn/dDzh3M+xEyylvMKMVzsKAPEqOK+xwYy8VimrwN1T6wycsW1rMHXNpAq02jlCqBMjKyI3pPm1xuPX+9Ohy7UIgoixlgiD0FgKMf9IZqIk2/3QzbaBKfqsAj+/9ZzxXjHc146xp6humImQ==~3162435~3748153; sec_cpt=6AFB146338AF1491B2A0A783C3E87EE2~1~YAAQtgrgegkjkVV8AQAAX8/baAXnqyewnq1AcqHgCwcZPoHndok9WVPr1mMRJWIj0eYghDCqVt0e8oh3RZNghB0VGQZW0PuVO6SbPpPqzt4zMcxQ2LSGHGxQxcDyMBnXUfZ1PBURZjLcNV40ueFJdU3i6ibTO2+86FXZU5rvR0/NjSKMpvNTGgOsQXFdT7MUVUuWKfr2yq6XTN3YKBSq//Re2nMem9FPFOI3sXG1LrZzDJ+WtbuXCyAVhV5a1bU0OOGQcp9GrKH82YeBY6RUuUb1YNkoUceeb7p163gnkP0bLqgb4PtSwTBwr+xhr2yUqmlbGyPRRVKWbb0CFoA5hiTAF1+K4Ucd4Hq0BEUkqOO3cPDsC2u+sESg5cSNKCSTCQiM+Rfj2wU9rqY2lySz+2uIv6y+uJbYcGmBQWWe8IrThk7PXDBgRZA0Kxsrw4ulp8tT6/Oy2jh0F0DPvt7EAhUoY3l1l65fqcA=; da_lid=6F461C239A72EA2BDA16BB990A787153DA|0|0|0; auth_state_KGk_Nvcut29Cdt6-nY0lDDh1Uqs=J5CT4M9RuoADXudT.Ek-NVVE6sDOcicgUClsfFigT2jxKzwhgRDMGNx1BdPg8D8cWJfkXdiP_PibfzC9plmkXEgJtIMU7-eWUxO7RSuERFrkrKfWsrIdiTmjf1vC9vzY8t498lKp87__xkoButP3ehDbnUi5JvvDHEicfzixQhLO8wqFQkqz7xVPHJzDZyuXWop_sprmSXRf4kTYSZw0osiuF2J9ZSKJStEQUTzdb1mVivsZIagSk6YfF2uHkZA39avWMeJunKjw5paPuwL_cb1FPnIfcAj6ZvSd0cefaxM4BJxsWk5Q6gtbaRiO1nrsoKgV8KkbQpHr014d-Uf374K4Lelv75_CtIUM-o906hTY0TnkY4tZg-4Dl79EnBglwGAr60e8Bt8IxY5Y17JerndNkVeh09O7c0LUOEV1JJbi3vAqcaiYUmJqrDI2o3DDCA0E5LWY--x1DW38z-JIWMvpHIKtdQI3XYfcJAoEi.agAPjkwLnwtG3DGsDcAMvA; ticontent=%2Ftistore; auth_state_VGmH6aPPVF9tac1coiW8wNLccBc=khggdY3NZ5jIFNeb.nIzBL8ytPNYA2VGJhrATK_lG6DklDuQlUM86j1GkE_a0sjmWfAcoR5QONcgCumL8WzKvGzij7ZnOhl-E2EQzblwwLyzk-G87vefQMHdoqUCryJUd51bHkviZMdUZJfRmmMh1cvp46eYllRUWjiePUtEfjYXjaLCsAaz4n2K_UcoH368sau_zN-tn_TE4bU9_b_JwkOCA_1gtVSh0qe7bXOLVu8ccq-OVZQZgjT3BvEObx4Jql0Jirw6Wpri_w0DPhTFbF6XnYpWC9eNHpvrHblRPNOr5dzLqqMbdi4FKdJRtseUe8XWeqPzG8goV2MO315xYrZrfXCN5qb52bHgHDNXLbPe5DUBFnmLQ56LRzM4veYBwtOSgNRF-XtHDIFUuORXLGXvVzGgDAeyBlT2J2wM6nKiQgP9t_mJkQBXb--rc7VTKXY294OL3ckvfDY9v6_ArWaB8XpUtZ9Va5YySndkb.gF_4qjUUl96QR7NFKbp7wA; user_pref_givenName=""; last-domain=www.ti.com.cn; ga_content_cookie=%2Ftistore; auth_state_Ux6UwqjFJebJGbotN3xG4vySv0U=MAju2-Zmjq1UX-NY.cdJ4hgsIeUIIKafJ5IR8ikHzaVQjufp3VMq0Ygjv3KOv3Fp8ksUGfNJJYXJipy8AdpbpE8RFJ_4jrBG-dLmSvWMSHsEGwxM-xDrSYuzKG-AY7XEHf0glFEfcEDouFch20pPiavlxL8wDk2AYPEgphvWB9V9KPtGqTzAx-dJh6OvaaikiYcfDw9w3gKO18cwcXkRv6SU_5A9gBFUdIMBaswpbCn-aTgxKafVl9Ft5lgKxOnn536oKXoIYYEdZBqAdk4wM_h-74Gz2NQV8plbIak-jJ0zav9R7TZAE_TQb3lpdXCroc0HizYm4gu5oCuiST_FN-lz0lrGFJqjRIb8gW-Xh5qQl9J7agGRkVr0DhDFQpInZYKDuN8j10B2ZLXCRxamKCSioDHQ9ReLBoskZtkH5nwdbSfmdOISPfb7KpNTgsOrN02XYMtCSGZnI9oxWeDuOuo_G1MQboxAz8zjgS3f7.tcpZj28BbEpRYTTs6MAkOQ; auth_state_eloAohaNdt_U9WIMlrKOD_ixcXw=aobmxUOdG3e7tGSy.tJjiwH2uU3e5t4vBFZ0XqIEmYchjfv_C5xUg_uyafX_ZRT6FXShdk3pSVMQh1t1AFti-tce4c4o5jyTbPhCpMJ1VYfWe45mWB1M0VhbY_EpbucG7fa9ZwhgINclBj1089qXasxlzc2I-U2ozpc86ySxGkKPmNu37UVznXWBEpEkME1tQRyNnHFtx_o1V8eiswryuueD16W3XkJn7s3XEnZpNoWMVkxi85miIlNRpDP2__0EROppjwIAeVDCT8UzTyBjcIoFcpwOfBkPJiRTqQlq1PDxNn89Hh5rAh1WbYjvJdSbeouN0vwaIdDB8jlNKm62esGvYXlmS56Du-yKpV2r4oRUlt7ch1Sg-h62bddPnseDlTbN--Az04L6u9gBsjszVXQXP14DpVNwitWzS0541kWa619VQcIfGxSXPjlh1kVqJveA3eJoOP1EqHxtP3wXl7h3XGt00u6yS7be3Yofz.pocr6gpYyUyycEoH26S4wg; tipage=%2Ftistore%2Fproduct%20page%20TAS5558DCA%20zh; tipageshort=product%20page%20TAS5558DCA%20zh; ga_page_cookie=product%20page%20TAS5558DCA%20zh; auth_state_Sqfg87xFJsDhmFoTXV_ztYtmS9U=6sg4Vo556of187aS.ChhN8_DJZA6MY4r2NMIxZQNDxFGOcssVYwnjO-WlRSv_2eFZX9qCu9PI_j358NRyyZZS_y_x81PyGcOFFbQ5cJQ1dx-4dHKXdMV3Ck2V36BqEWusu0d9ygHBuyuDx2nABONnQeWYlQTzmfoLNPIH0GsoGUXBnU1QuUyKxQOZuWeqfDYO9YwUlDHEVszws7lfXbRgxAH4cEiC5DTElN-UbElMKvOVH2ewWoGnewFZrOzMSLUSZG3gDhsfYVdQktA-K5pCOxwKIqf32BMn3sbgHrjTfHYtylw13X8LdePW0BeGVdRW9I-WHOGDxY7nFvFaNEwajnWSwajW9k0oAO51gv5VH0R3arqwSZ0Qn5pLJOKFVWXYpDLEcUu8s6g1TDrAFiGbCuHmDfMxI7bopUCbVEX8bR-SSS15HKLNkfZ7XoA-6LnCiWSuudfLcDh2VUtlWRrKE6bQGmew0dJ-11mNVYb9.PAyF_QFUu4opk1SY3KxGIw; ABTasty=uid=j6wshax2z59xfgv8&fst=1632830177486&pst=1633842033600&cst=1633845315012&ns=10&pvt=136&pvis=11&th=686831.851794.89.11.5.1.1632830480571.1633847690841.1_759046.943435.6.6.1.1.1632907981896.1632924253873.1; ak_bmsc=73C01BA0697DC1026242A104E2379461~000000000000000000000000000000~YAAQeRTSPC1lBVl8AQAAFA4DaQ0FhUuvoeeJJpNdTzh+hejszYvRTYWwO+M7NgmlhzM95PvEW2nS8omqe6BAdXBulKauDNOWVX+Ls8swAL9RKufZl5mAa5RyTqAkUaMdfgFOnWyZOnrCku7ql9KtqN6vDXiBnIKANNUZU0ptCUb+RXOLusRB3nUj2txqhL/D8Z1svG9ctUYKgxx9tvbv6izJWx7jFvtQIi3uVYLLJKSggV0kwqW+WoaWis9+/UaT1E3jEGzw4FdOj/V1bTtSajwwKXkx0i7abrMFJ0GYqjW6qdgp1FkKOq5WKMB30P1b342pcG4sU3QAIn2TYma8K//LJl75zWwo6QH3d6ojIS6kqRIbiClEdLq0WiB0CsFX; utag_main=v_id:017c2c433e580045588fc3c4eb1403078002607000bd0$_sn:9$_ss:0$_st:1633851356930$free_trial:false$dc_visit:3$_pn:18%3Bexp-session$ses_id:1633842032152%3Bexp-session$dc_event:6%3Bexp-session$dc_region:eu-west-1%3Bexp-session; ti_rid=1924cf0e; bm_sv=A0CA27D42DAEFF35593D80ABAC9A8202~/0W+Lb67BJBFwj2/ZlYdDtTFt34adiaJnPVL5w54P7/L9C53a/cN9qbHt1A3zNQQK4+nTFUI4jKIQzXktoqeT0y/u0elZlwWB/1ftJ4OB8+ePT6UKrxuBb/3XzbotygCKxXOw7zC6EdsAVj5cdYEtmiiUE1qOC+qYxlr1y0rAgI=; _abck=D98E4E551CDCA02D2A26334F85012BB5~-1~YAAQtgrgen1RlVV8AQAA2Z4LaQYMmv13Mg+kfpc5LdAkiN/+Iumf3XW2S5Vb7Ue985kaE43SHiPj9LRXihV/hboRsCtKlSkipizbnCym1+5QfFhUdDqTk3uOSd/dhWGRh9Z44srgVzER8NrzZHelG26hw/TYa07PV7zo1N0MZBUJaJonRbkOVUzHQsXRfgWRErtlcT21LyFAjlQJ6bjX+pHfCsuPYIlKPl9uXrqdO+HPKbaHvmnswPFQpG555PouhSBXFaVYg6PPlsAvRIjcodDMpUz9gFBrfS5Whh721TmOa0aD0dth/sLW77lKr2PHrR/1otdIsjBBqTpW33I/M1n4Gk1DLJv969x0GR/bpt99JS5LdXI8motc9Lyxih13Zxgtl8HLQo7xd2X7fRsQHHF07s5YEDtA8riOAmN8TUZaLpoF9WmBeDQhydoExgDML2AhkA==~0~-1~-1'
    }

    # json类型的参数
    addtocartJson = {"cartRequestList":[{"opnId":"BQ7692006PWR","quantity":"1","tiAddtoCartSource":"store-pdp","dienCode":"","year":"","week":"","batchCode":"","pcrCode":"","sparam":""}],"currency":"CNY"}
    clickJson = {"sensor_data":"7a74G7m23Vrp0o5c9280521.7-1,2,-94,-100,Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36,uaend,12147,20030107,zh-CN,Gecko,5,0,0,0,402004,7688422,1440,877,1440,900,1440,210,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:1,bat:1,x11:0,x12:1,8924,0.693631127346,816923844210.5,0,loc:-1,2,-94,-101,do_en,dm_en,t_en-1,2,-94,-105,0,-1,0,0,1049,-1,1;0,-1,0,0,1153,-1,0;-1,2331,-94,-12202,0,0,0,0,-1,-1,0;0,-1,0,0,1049,-1,1;0,-1,0,0,1153,-1,0;-1,2,-94,-108,0,1,11090,91,0,2,-1;1,2,11234,-2,0,0,-1;2,1,23089,-2,0,0,-1;3,3,23091,-2,0,0,-1;4,2,23214,-2,0,0,-1;5,1,29627,91,0,2,-1;6,2,29787,-2,0,0,-1;7,1,53104,91,0,2,-1;8,2,53622,-2,0,0,-1;9,1,181147,91,0,2,-1;10,2,181299,-2,0,0,-1;11,1,189496,91,0,2,-1;12,2,189823,-2,0,0,-1;13,1,298694,91,0,2,-1;14,2,299129,-2,0,0,-1;15,1,726279,91,0,2,-1;16,2,726450,-2,0,0,-1;17,1,737808,17,0,4,-1;18,1,903543,91,0,2,-1;19,2,904044,-2,0,0,-1;20,1,916128,91,0,2,-1;21,2,916501,-2,0,0,-1;-1,2,-94,-110,0,1,16847,696,390;1,1,16848,696,390;2,1,16850,694,376;3,1,16858,693,365;4,1,16865,689,345;5,1,16873,689,338;6,1,16881,687,324;7,1,16891,687,311;8,1,16898,687,300;9,1,16905,687,291;10,1,16914,687,282;11,1,16922,687,278;12,1,16931,687,273;13,1,16940,689,271;14,1,16946,689,269;15,1,16955,690,268;16,1,16964,690,267;17,1,16972,691,267;18,1,16980,691,267;19,1,17055,691,268;20,1,17061,691,271;21,1,17069,691,273;22,1,17079,690,276;23,1,17085,689,279;24,1,17093,689,284;25,1,17101,689,286;26,1,17109,689,289;27,1,17119,689,291;28,1,17127,689,293;29,1,17134,690,294;30,1,17143,695,295;31,1,17151,704,295;32,1,17160,712,295;33,1,17169,723,295;34,1,17175,732,295;35,1,17183,746,295;36,1,17191,757,295;37,1,17199,771,295;38,1,17208,785,295;39,1,17216,802,295;40,1,17223,816,294;41,1,17231,830,294;42,1,17240,843,294;43,1,17248,857,292;44,1,17257,869,292;45,1,17264,880,291;46,1,17273,894,289;47,1,17281,907,286;48,1,17290,921,283;49,1,17297,935,277;50,1,17306,949,272;51,1,17313,960,267;52,1,17321,974,261;53,1,17330,985,255;54,1,17338,990,252;55,1,17346,1007,245;56,1,17356,1011,244;57,1,17363,1020,241;58,1,17370,1025,239;59,1,17381,1030,237;60,1,17387,1034,236;61,1,17396,1038,235;62,1,17404,1041,235;63,1,17412,1043,235;64,1,17421,1044,234;65,1,17428,1045,234;66,1,17437,1047,233;67,1,17445,1047,233;68,1,17455,1048,233;69,1,17460,1049,232;70,1,17469,1049,232;71,1,17477,1050,232;72,1,17494,1050,232;73,1,17550,1050,232;74,1,17640,1050,232;75,1,17651,1050,235;76,1,17657,1050,239;77,1,17664,1049,242;78,1,17672,1046,246;79,1,17683,1044,250;80,1,17688,1041,254;81,1,17697,1037,258;82,1,17705,1031,265;83,1,17715,1027,268;84,1,17721,1020,274;85,1,17729,1014,279;86,1,17737,1012,280;87,1,17746,1006,285;88,1,17753,1002,287;89,1,17761,997,290;90,1,17769,992,292;91,1,17778,987,294;92,1,17789,981,297;93,1,17794,976,298;94,1,17802,969,301;95,1,17810,965,302;96,1,17818,960,303;97,1,17827,955,304;98,1,17834,952,305;99,1,17843,948,307;253,3,22957,1092,262,-1;254,4,23000,1092,262,-1;255,2,23015,1092,262,-1;309,3,25346,1128,299,-1;310,4,25385,1128,299,-1;311,2,25389,1128,299,-1;487,3,174399,961,261,-1;488,4,174419,961,261,-1;489,2,174423,961,261,-1;572,3,175727,1101,297,-1;573,4,175767,1101,297,-1;574,2,175771,1101,297,-1;686,3,293731,954,257,-1;687,4,293749,954,257,-1;688,2,293752,954,257,-1;748,3,295244,1078,279,-1;749,4,295291,1078,279,-1;750,2,295294,1078,279,-1;1030,3,720095,944,253,-1;1031,4,720114,944,253,-1;1032,2,720117,944,253,-1;1081,3,721213,1137,285,-1;1082,4,721259,1137,285,-1;1083,2,721262,1137,285,-1;1207,3,783497,955,267,-1;1208,4,783508,955,267,-1;1209,2,783510,955,267,-1;1247,3,785076,1110,282,-1;1248,4,785107,1110,282,-1;1249,2,785110,1110,282,-1;1351,3,900363,948,261,-1;1352,4,900375,948,261,-1;1353,2,900378,948,261,-1;1408,3,902188,1122,298,-1;1409,4,902236,1122,298,-1;1410,2,902239,1122,298,-1;2474,3,1868198,959,257,-1;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,2,11241;0,11272;3,16288;1,16339;2,20242;3,22954;2,29796;0,29811;3,45214;1,45255;2,56664;0,77369;1,92843;0,121496;1,144545;0,164039;1,173278;3,174394;2,181307;0,181332;3,188689;1,188758;2,193340;0,199303;1,251654;0,278403;1,292245;3,293728;2,303083;0,305681;1,326903;0,349784;1,479958;0,493965;1,526808;0,527384;1,556536;0,562251;1,633338;0,633831;1,684447;0,692441;1,717922;3,720092;2,726458;0,726800;3,733875;1,733987;2,738125;0,743411;1,743658;0,746562;1,768300;0,771584;1,774680;3,783495;2,791686;0,823823;1,863589;0,869518;1,895328;3,900359;2,916507;0,916818;3,925437;1,925548;2,929127;0,949641;1,1039821;0,1045798;1,1051279;0,1104227;1,1109458;0,1244857;1,1261138;0,1285323;1,1310747;0,1315927;1,1337491;0,1344322;1,1360014;0,1378598;1,1398505;3,1868194;-1,2,-94,-112,https://www.ti.com.cn/store/ti/zh/p/product/?p=TAS5558DCA-1,2,-94,-115,7429277,21204071,32,0,0,0,28633315,1868198,0,1633847688421,16,17478,22,2475,2913,25,0,1868200,28429316,0,D98E4E551CDCA02D2A26334F85012BB5~-1~YAAQeRTSPHctBll8AQAASTwFaQYgbe9FuVzouuk4kLJN4j+znuM//4ljHvM0BeBdCM+p6HoHEbDDPMGqjs3hkANb3FpJToJ22/y9h+2nfJ+rGuSfmg3XACyxQ2maYoynBTlupiyjdvRk3uhceI93oJ5zBI9dC16RnWUwLgbonE0Hvcb0HAyny91YjekAtFkX3UyhakVLP50mNcjWstw8SCNHjxjuVT2hbesArhyowrGQQ8Ii/rCNW7lR9/RETA2WubdIqGy1CCU2dY6F1HSS8b2zZ6E6Kz5FrOZx8cooWXfLboNhpJkZH05CYd+G+NzOlX/YUaV+Ymib49XcJN7UnlbTtPhtlWk7G+sLe2Gm4dsmBYmmBYnmCImw6Jusjl4HfwDborRCQCXoHlmU83NRA+JR+jTpPWs5U5tnOkZGZ6k54fFKcxLknrnT1SPT56pQY7sCMwU=~-1~-1~-1,41986,681,-907721962,30261693,PiZtE,106375,70,0,-1-1,2,-94,-106,1,16-1,2,-94,-119,40,40,20,40,40,40,20,20,20,0,0,0,20,260,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,10321144241322243122-1,2,-94,-70,-327719108;859937113;dis;,7;true;true;true;-480;true;30;30;true;false;-1-1,2,-94,-80,5435-1,2,-94,-116,9341425440-1,2,-94,-118,306917-1,2,-94,-129,6f625ae26685dace6d6daabf406381f25a34a9df1effbb3a82ff4d63834b7dbd,2,50e6eb9f9ecc497346c1addd763b2f10c2af420def36a636140b2380740b0758,Google Inc. (Intel Inc.),ANGLE (Intel Inc., Intel(R) Iris(TM) Plus Graphics OpenGL Engine, OpenGL 4.1 INTEL-14.7.4),5d46e782775916804ffc6ea60cfa44fb08a21a9cddbc005eb9996c50f34ea1a4,32-1,2,-94,-121,;8;13;0"}

    response = requests.post(url=click_url, json=clickJson, headers=header)
    print(response.text)
    # 发送post请求
    response = requests.post(url=addtocart_url, json=addtocartJson, headers=header)
    print(response.text)

class myThread(threading.Thread):

    def __init__(self, productCode):
        threading.Thread.__init__(self)
        self.productCode = productCode

    def run(self):
        # print("开始线程：" + self.productCode)
        autoBuyProductByCode(self.productCode)
        # print("退出线程：" + self.productCode)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logger.info('==================PyCharm Start====================')
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    loopProductListToGetInventory()

    # 通过url直接加上请求参数，与通过params传参效果是一样的

    # getUrl('https://www.ti.com.cn/storeservices/cart/opninventory?opn=HD3SS3212IRKSR')

    # 通过params传参
    # print(response.text)  # 打印状态码
    # print(response.text)		# 获取响应内容
# addtocart("PLL1707IDBQRQ1")
logger.info('==================PyCharm End====================')
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
