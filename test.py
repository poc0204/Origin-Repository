
import pymysql
import threading
from dbutils.pooled_db import PooledDB, SharedDBConnection
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import os
load_dotenv()

# POOL = PooledDB(
#     creator=pymysql,  # 使用連結資料庫的模組
#     maxconnections=6,  # 連線池允許的最大連線數，0和None表示不限制連線數
#     mincached=2,  # 初始化時，連結池中至少建立的空閒的連結，0表示不建立
#     maxcached=5,  # 連結池中最多閒置的連結，0和None不限制
#     maxshared=3,  # 連結池中最多共享的連結數量，0和None表示全部共享。PS: 無用，因為pymysql和MySQLdb等模組的 threadsafety都為1，所有值無論設定為多少，_maxcached永遠為0，所以永遠是所有連結都共享。
#     blocking=True,  # 連線池中如果沒有可用連線後，是否阻塞等待。True，等待；False，不等待然後報錯
#     maxusage=None,  # 一個連結最多被重複使用的次數，None表示無限制
#     setsession=[],  # 開始會話前執行的命令列表。如：["set datestyle to ...", "set time zone ..."]
#     ping=0,
#     # ping MySQL服務端，檢查是否服務可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
#     host=os.getenv('host'),
#     port=3306,
#     user=os.getenv('user'),
#     password=os.getenv('password'),
#     database=os.getenv('database'),
#     charset='utf8'
# )


# def func():
#     # 檢測當前正在執行連線數的是否小於最大連結數，如果不小於則：等待或報raise TooManyConnections異常
#     # 否則
#     # 則優先去初始化時建立的連結中獲取連結 SteadyDBConnection。
#     # 然後將SteadyDBConnection物件封裝到PooledDedicatedDBConnection中並返回。
#     # 如果最開始建立的連結沒有連結，則去建立一個SteadyDBConnection物件，再封裝到PooledDedicatedDBConnection中並返回。
#     # 一旦關閉連結後，連線就返回到連線池讓後續執行緒繼續使用。
#     try:
#         conn = POOL.connection()
#         print('連結被拿走了', conn._con)
#         print('池子裡目前有', POOL._idle_cache, '\r\n')

#         cursor = conn.cursor()
#         cursor.execute('select * from level2')
#         result = cursor.fetchall()
#         print(result)
#         conn.close()
#     except:
#         conn.rollback()


# func()






POOL = PooledDB(
    creator=pymysql,  # 使用連結資料庫的模組
    maxconnections=6,  # 連線池允許的最大連線數，0和None表示不限制連線數
    mincached=2,  # 初始化時，連結池中至少建立的空閒的連結，0表示不建立
    maxcached=5,  # 連結池中最多閒置的連結，0和None不限制
    maxshared=3,  # 連結池中最多共享的連結數量，0和None表示全部共享。PS: 無用，因為pymysql和MySQLdb等模組的 threadsafety都為1，所有值無論設定為多少，_maxcached永遠為0，所以永遠是所有連結都共享。
    blocking=True,  # 連線池中如果沒有可用連線後，是否阻塞等待。True，等待；False，不等待然後報錯
    maxusage=None,  # 一個連結最多被重複使用的次數，None表示無限制
    setsession=[],  # 開始會話前執行的命令列表。如：["set datestyle to ...", "set time zone ..."]
    ping=0, 
    # ping MySQL服務端，檢查是否服務可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
    host=os.getenv('host'),
    port=3306,
    user=os.getenv('user'),
    password=os.getenv('password'),
    database=os.getenv('database'),
    charset='utf8'
)
 
def func():
    # 檢測當前正在執行連線數的是否小於最大連結數，如果不小於則：等待或報raise TooManyConnections異常
    # 否則
    # 則優先去初始化時建立的連結中獲取連結 SteadyDBConnection。
    # 然後將SteadyDBConnection物件封裝到PooledDedicatedDBConnection中並返回。
    # 如果最開始建立的連結沒有連結，則去建立一個SteadyDBConnection物件，再封裝到PooledDedicatedDBConnection中並返回。
    # 一旦關閉連結後，連線就返回到連線池讓後續執行緒繼續使用。
    conn = POOL.connection()

    # print(th, '連結被拿走了', conn1._con)
    # print(th, '池子裡目前有', pool._idle_cache, '\r\n')

    cursor = conn.cursor()
    cursor.execute('select * from level2')
    result = cursor.fetchall()
    conn.close()
    print(result)

func()
# print(link_mysql())
# cursor = connection.cursor()
# sql = "select  COUNT(id) from level2; "
# cursor.execute(sql)
# id_count = cursor.fetchall()
# print(id_count)