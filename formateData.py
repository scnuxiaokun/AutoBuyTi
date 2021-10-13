import requests,json
import _thread,threading
import urllib3
import logging
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import threading, queue
def getParentCode(productCode):
    url = "https://www.ti.com.cn/search/opn?searchTerm="+productCode
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        parentCode = json.loads(response.text).get('genericPartNumber');
        print("productCode:"+productCode+" parentCode:"+parentCode)
        return (productCode, parentCode)
    else:
        print("ERROR code="+str(response.status_code))
    return 0

if __name__ == '__main__':
    result = {}
    productCodeMap = {}
    f = open("data.txt")
    lines = f.readlines()
    f.close()

    productCodeList = []
    for index in range(len(lines)):
        line = lines[index]
        productCode = line.replace('\n', '').replace('\r', '').strip()
        productCodeList.append(productCode)

    executor = ThreadPoolExecutor(max_workers=1)
    tasks = [executor.submit(getParentCode, (item)) for item in productCodeList]
    for task in as_completed(tasks):
        (productCode, parentCode) = task.result()
        productCodeMap[productCode] = parentCode

    print(productCodeMap)

    for productCode, parentCode in productCodeMap.items():
        if parentCode in result:
            result[parentCode].append(productCode)
        else:
            result[parentCode] = [productCode]

    print(result)
    fo = open("formattedData.json", "w")
    fo.write(json.dumps(result))
    fo.close()