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
import random
import proxy
import common
import order


def getInventory(url):
    # logger.info("请求URL:"+url)
    # response = requests.get(url=url)
    response = proxy.getV2(url)
    if response.status_code == 200:
        return json.loads(response.text).get('inventory')
    else:
        logger.error("[ERROR]:"+" status_code:"+ str(response.status_code)+ " "+url)  # 打印状态码
        return -1

def autoBuyProductByCode(productCode):
    url = 'http://www.ti.com.cn/storeservices/cart/opninventory?opn=' + productCode + "&abc=123"
    t = time.time()
    inventory = getInventory(url)
    t = str(time.time() - t)
    processHasInventory(productCode, inventory, t)

def autoBuyProductByCodeV2(parentCode, productCodeList):
    blackList = ["HD3SS460RHRT","TCAN1043GDMTRQ1", "TPS25944LRVCR", "TPS544B20RVFR", "TCAN4550RGYR", "TPS53317RGBR", "TPS63805YFFT"]
    # 过滤掉有库存但不能买的商品
    for code in productCodeList:
        if code in blackList:
            return
    t = time.time()
    url = "https://www.ti.com.cn/productmodel/"+parentCode+"/tistore"
    response = proxy.getV2(url)
    t = str(time.time() - t)
    if response.status_code == 200:
        list = json.loads(response.text)
        productCodeMap = {}
        for code in productCodeList:
            productCodeMap[code] = 1

        for item in list:
            productCode = item['orderablePartNumber']
            inventory = item['inventory']
            if productCode in productCodeMap:
                processHasInventory(productCode, int(inventory), t)
    else:
        logger.error("[ERROR]:" + " status_code:" + str(response.status_code) + " " + url)  # 打印状态码

def processHasInventory(productCode, inventory, timespent):
    t = timespent
    if inventory > 0 :
        f = open("inventory.txt", "a")
        f.write(productCode + "," + str(inventory) + "\n")
        f.close()
        logger.info("["+productCode+"]" + "库存数量:" + str(inventory)  + "t=" + t)
    elif inventory == 0:
        logger.info("[" + productCode + "]" + "没库存" + "t=" + t)
    else:
        logger.info("[" + productCode + "]" + "查询失败" + "t=" + t)

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

def loopProductListToGetInventoryV2():
    maxThreadCount = 10
    executor = ThreadPoolExecutor(max_workers=maxThreadCount)

    fo = open("formattedData.json")
    formattedData = fo.read()
    parentCodeMap = json.loads(formattedData)

    all_task=[]
    index = 0
    keys = list(parentCodeMap.keys())
    while 1:
        parentCode = keys[index]
        productCodeList = parentCodeMap[parentCode]
        all_task.append(executor.submit(autoBuyProductByCodeV2, parentCode, productCodeList))
        if len(all_task) >= maxThreadCount :
            copy_all_task = all_task
            for future in as_completed(copy_all_task):
                all_task.remove(future)
                if len(all_task) < maxThreadCount:
                    break
        index = index+1
        if index >= len(keys) :
            index = 0

    logger.info("===========全部完成===========")

def loopProductListToGetInventory():
    maxThreadCount = 500
    maxIpCount = 100
    executor = ThreadPoolExecutor(max_workers=maxThreadCount)
    all_task = []
    productCodeQueue = queue.SimpleQueue()

    while 1:
        productCodeList = getProductList(productCodeQueue, maxIpCount)
        tasks = [executor.submit(autoBuyProductByCode, (item)) for item in productCodeList]
        for task in tasks:
            all_task.append(task)

        if len(all_task) >= maxThreadCount :
            copy_all_task = all_task

            for future in as_completed(copy_all_task):
                all_task.remove(future)
                if len(all_task) <= maxThreadCount - maxIpCount:
                    break

    logger.info("===========全部完成===========")

def addtocart(productCode):
    response = order.addtocart(productCode)
    logger.info(response.status_code)
    logger.info(response.text)
# Press the green button in the gutter to run the script.
# 创建Logger
logger = common.initLoger()

if __name__ == '__main__':
    logger.info('==================PyCharm Start====================')

    loopProductListToGetInventoryV2()
    # autoBuyProductByCodeV2("BQ29209", ["BQ29209DRBR"])
    # autoBuyProductByCode("BQ7692000PWR")

    # 通过url直接加上请求参数，与通过params传参效果是一样的

    # addtocart("PLL1707IDBQRQ1")
    logger.info('==================PyCharm End====================')
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
