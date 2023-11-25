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
            SELECT DATE_FORMAT(ts, '%d') AS day, MONTH(ts) as month, YEAR(ts) as year, HOUR(ts) as hour, AVG(value) 
            FROM `main` 
            WHERE param = "temp" 
            GROUP BY year, month,day,hour 
            ORDER BY year,month, day,hour  
            DESC LIMIT 1
            """)
        result = [models.LatestTemp(*row) for row in cs.fetchall()]
        return result
    
def latest_average_pm25():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT DATE_FORMAT(ts, '%d') AS day, MONTH(ts) as month, YEAR(ts) as year, HOUR(ts) as hour, AVG(value) 
            FROM `main` 
            WHERE param = "pm25" 
            GROUP BY year, month,day,hour 
            ORDER BY year,month, day,hour 
            DESC LIMIT 1
            """)
        result = [models.LatestPm25(*row) for row in cs.fetchall()]
        return result
    
def latest_average_sound():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT DATE_FORMAT(ts, '%d') AS day, MONTH(ts) as month, YEAR(ts) as year, HOUR(ts) as hour, AVG(value) 
            FROM `main` 
            WHERE param = "sound" 
            GROUP BY year, month,day,hour 
            ORDER BY year,month, day,hour 
            DESC LIMIT 1
            """)
        result = [models.LatestSound(*row) for row in cs.fetchall()]
        return result
    
def latest_count():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT DATE_FORMAT(ts, '%d') AS day, MONTH(ts) as month, YEAR(ts) as year, HOUR(ts) as hour, COUNT(value) 
            FROM `main`
            WHERE param = "humcount" 
            GROUP BY year, month,day,hour 
            ORDER BY year,month, day,hour
            DESC LIMIT 1
            """)
        result = [models.LatestCount(*row) for row in cs.fetchall()]
        return result

def latest_average_hum():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT DATE_FORMAT(ts, '%d') AS day, MONTH(ts) as month, YEAR(ts) as year, HOUR(ts) as hour, AVG(value) 
            FROM `main` 
            WHERE param = "hum" 
            GROUP BY year, month,day,hour 
            ORDER BY year,month, day,hour 
            DESC LIMIT 1
            """)
        result = [models.LatestHum(*row) for row in cs.fetchall()]
        return result