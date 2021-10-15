import logging,json

def initLoger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 创建Handler

    # 终端Handler
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)

    # 文件Handler
    fileHandler = logging.FileHandler('log.log', mode='a', encoding='UTF-8')
    fileHandler.setLevel(logging.NOTSET)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    consoleHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)

    # 添加到Logger中
    logger.addHandler(consoleHandler)
    logger.addHandler(fileHandler)
    return logger

def getCookie():
    f = open("driver_cookie.txt")
    cookieString = f.read()
    f.close()
    cookieList = json.loads(cookieString)
    result = []
    for cookieItem in cookieList:
        name = cookieItem['name']
        value = cookieItem['value']
        result.append(name+"="+value)

    return "; ".join(result)