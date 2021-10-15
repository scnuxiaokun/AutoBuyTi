import requests,json
import _thread,threading
import urllib3
import logging
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import threading, queue
import proxy
import common

def getParentCode(productCode):
    url = "http://www.ti.com.cn/search/opn?searchTerm="+productCode

    try:
        response = proxy.getV3(url)
        if response.status_code == 200:
            map = json.loads(response.text)
            if 'genericPartNumber' in map:
                parentCode = map.get('genericPartNumber');
                logger.info("productCode:"+productCode+" parentCode:"+parentCode)
                return (productCode, parentCode)
        else:
            logger.info("ERROR code="+str(response.status_code))
    except BaseException as Argument:
        logger.error("Exception:"+str(Argument)+" url:"+url)
    else:
        pass
    return 0

# 创建Logger
logger = common.initLoger()
if __name__ == '__main__':
    productCodeMap = {}
    f = open("data.txt")
    lines = f.readlines()
    f.close()

    fo = open("formattedData.json")
    formattedData = fo.read()
    result = json.loads(formattedData)
    fo.close()
    productCodeMapInFile = {}
    for parentCode, codeList in result.items():
        for code in codeList:
            productCodeMapInFile[code] = 1

    productCodeList = []
    for index in range(len(lines)):
        line = lines[index]
        productCode = line.replace('\n', '').replace('\r', '').strip()
        if productCode in productCodeMapInFile:
            pass
        else:
            productCodeList.append(productCode)

    executor = ThreadPoolExecutor(max_workers=1)
    tasks = [executor.submit(getParentCode, (item)) for item in productCodeList]
    for task in as_completed(tasks):
        try:
            (productCode, parentCode) = task.result()
            productCodeMap[productCode] = parentCode
        except BaseException as Argument:
            logger.error("Exception:" + str(Argument))
        else:
            pass

    logger.info(productCodeMap)

    for productCode, parentCode in productCodeMap.items():
        if parentCode in result:
            result[parentCode].append(productCode)
        else:
            result[parentCode] = [productCode]

    for parentCode, codeList in result.items():
        result[parentCode] = list(set(codeList))
    logger.info(result)
    fo = open("formattedData.json", "w")
    fo.write(json.dumps(result))
    fo.close()