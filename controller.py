import sys
from flask import abort
import pymysql
from dbutils.pooled_db import PooledDB
from config import OPENAPI_STUB_DIR, DB_HOST, DB_USER, DB_PASSWD, DB_NAME

sys.path.append(OPENAPI_STUB_DIR)
from swagger_server import models

pool = PooledDB(creator=pymysql,
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWD,
                database=DB_NAME,
                maxconnections=1,
                blocking=True)

def latest_average_temperature():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT DATE(ts), HOUR(ts), AVG(value) 
            FROM `main` 
            WHERE param = "temp" 
            GROUP BY DATE(ts),HOUR(ts) 
            ORDER BY DATE(ts),HOUR(ts) DESC LIMIT 1
            """)
        result = [models.LatestTemp(*row) for row in cs.fetchall()]
        return result
    
def latest_average_pm25():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT DATE(ts), HOUR(ts), AVG(value) 
            FROM `main` 
            WHERE param = "pm25" 
            GROUP BY DATE(ts),HOUR(ts) 
            ORDER BY DATE(ts),HOUR(ts) DESC LIMIT 1
            """)
        result = [models.LatestTemp(*row) for row in cs.fetchall()]
        return result