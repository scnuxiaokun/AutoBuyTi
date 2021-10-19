import sqlite3,time
from enum import IntEnum
import common

class InventoryStatus(IntEnum):
    Init = 0
    Process = 10
    Finish = 20
    Fail = 30

def initAutoBuyTiDB():
    con = sqlite3.connect('autoBuyTi.db')
    con.row_factory = dict_factory
    cur = con.cursor()

    inventoryCreateTableSQL = "CREATE TABLE IF NOT EXISTS inventory(" \
                     "id INTEGER PRIMARY KEY, " \
                     "product_code TEXT NOT NULL, " \
                     "stock NUMBER NOT NULL, " \
                      "status NUMBER NOT NULL, " \
                      "process_count NUMBER NOT NULL," \
                     "create_time TEXT NOT NULL, " \
                      "update_time TEXT NOT NULL" \
                      ")"
    result = cur.execute(inventoryCreateTableSQL)

    con.commit()
    return con

def insertInventory(con, product_code, stock):
    t = common.formatTime(time.localtime())
    sql = "INSERT INTO inventory VALUES(NULL,?,?,?,?,?,?)"
    cur = con.cursor()
    cur.execute(sql, (product_code, stock, int(InventoryStatus.Init), 0, t, t))
    con.commit()

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# 查询状态为statusList的商品
# 返回值说明：
# product_code 商品型号
# stock 商品库存
def selectInventory(con, statusList):
    statusStrList = []
    for status in statusList:
        statusStrList.append(str(int(status)))
    statusStrList = ",".join(statusStrList)
    sql = "SELECT * FROM inventory WHERE status in ({statusStrList})".format(statusStrList=statusStrList);
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    return cur.fetchall()

# 查询需要下单的商品
def selectProductListForAutoBuy(con):
    statusList = [InventoryStatus.Init, InventoryStatus.Process]
    statusStrList = []
    for status in statusList:
        statusStrList.append(str(int(status)))
    statusStrList = ",".join(statusStrList)
    sql = "SELECT * FROM inventory WHERE status in ({statusStrList}) AND process_count<3".format(statusStrList=statusStrList);
    cur = con.cursor()
    cur.execute(sql)
    con.commit()

# 标记商品尝试下单一次
def tryAutoBuyInventory(con, id):
    t = common.formatTime(time.localtime())
    sql = "UPDATE inventory set process_count=process_count+1, update_time='{time}' where id={id}".format(time=t, id=id)
    cur = con.cursor()
    cur.execute(sql)
    con.commit()

# 标记商品下单完成
def finishAutoBuyInventory(con, id):
    t = common.formatTime(time.localtime())
    sql = "UPDATE inventory set status={status}, update_time='{time}' where id={id}".format(status=int(InventoryStatus.Finish), time=t, id=id)
    cur = con.cursor()
    cur.execute(sql)
    con.commit()

# 标记商品下单失败
def failAutoBuyInventory(con, id):
    t = common.formatTime(time.localtime())
    sql = "UPDATE inventory set status={status}, update_time='{time}' where id={id}".format(status=int(InventoryStatus.Fail), time=t, id=id)
    cur = con.cursor()
    cur.execute(sql)
    con.commit()


# 例子
# con = initAutoBuyTiDB()
# insertInventory(con, "abc", 123)
# list = selectInventory(con, [InventoryStatus.Init, InventoryStatus.Process])
# tryAutoBuyInventory(con, list[0]['id'])
# list = selectInventory(con, [InventoryStatus.Init, InventoryStatus.Process])
# print(list)