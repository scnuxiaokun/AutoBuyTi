import logging

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