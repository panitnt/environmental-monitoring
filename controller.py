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

def latest_average(param):
    day_format = '%d'
    if param == 'humcount':
        with pool.connection() as conn, conn.cursor() as cs:
            cs.execute("""
                SELECT CONVERT(DATE_FORMAT(ts, %s), SIGNED) AS day, 
                    MONTH(ts) as month, 
                    YEAR(ts) as year, 
                    HOUR(ts) as hour, 
                    SUM(value) as value
                FROM `main` 
                WHERE param=%s
                GROUP BY year, month,day,hour 
                ORDER BY year,month, day,hour  
                DESC LIMIT 1
                """,[day_format,param])
            result = cs.fetchone()
        if result:
            return models.Latest(*result)
        else:
            abort(404)
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT CONVERT(DATE_FORMAT(ts, %s), SIGNED) AS day, 
                MONTH(ts) as month, 
                YEAR(ts) as year, 
                HOUR(ts) as hour, 
                AVG(value) as value
            FROM `main` 
            WHERE param=%s
            GROUP BY year, month,day,hour 
            ORDER BY year,month, day,hour  
            DESC LIMIT 1
            """,[day_format,param])
        result = cs.fetchone()
    if result:
        return models.Latest(*result)
    else:
        abort(404)
    
def all_average(param):
    day_format = '%d'
    if param == 'humcount':
        with pool.connection() as conn, conn.cursor() as cs:
            cs.execute("""
            SELECT CONVERT(DATE_FORMAT(ts, %s), SIGNED) AS day, 
                MONTH(ts) as month, 
                YEAR(ts) as year, 
                HOUR(ts) as hour, 
                SUM(value) as value
            FROM `main` 
            WHERE param=%s 
            GROUP BY year, month,day,hour ORDER BY year,month, day,hour  
            DESC
            """,[day_format,param])
            result = [models.AllAvg(*row) for row in cs.fetchall()]
            return result
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
        SELECT CONVERT(DATE_FORMAT(ts, %s), SIGNED) AS day, 
            MONTH(ts) as month, 
            YEAR(ts) as year, 
            HOUR(ts) as hour, 
            AVG(value) as value
        FROM `main` 
        WHERE param=%s 
        GROUP BY year, month,day,hour ORDER BY year,month, day,hour  
        DESC
        """,[day_format,param])
        result = [models.AllAvg(*row) for row in cs.fetchall()]
        return result
