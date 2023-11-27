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
            return models.AverageValue(*result)
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
        return models.AverageValue(*result)
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
            result = [models.AverageValue(*row) for row in cs.fetchall()]
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
        result = [models.AverageValue(*row) for row in cs.fetchall()]
        return result

def param_separate_source(param):
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
        SELECT source, AVG(lat) as lat, AVG(lon) as lon
        FROM `main` 
        WHERE param=%s 
        GROUP BY source
        """,[param])
        result = [models.SourceParam(*row) for row in cs.fetchall()]
        return result
    
def hour_average_value(param):
    if param == 'humcount':
        with pool.connection() as conn, conn.cursor() as cs:
            cs.execute("""
            SELECT source,
                CONVERT(DATE_FORMAT(ts, %s), SIGNED) AS day, 
                MONTH(ts) as month, 
                YEAR(ts) as year, 
                HOUR(ts) as hour, 
                SUM(value) as value
            FROM `main` 
            WHERE param=%s 
            GROUP BY source, year, month,day,hour 
            ORDER BY source, year,month, day,hour  
            """,['%d',param])
            result = [models.HourAverageValue(*row) for row in cs.fetchall()]
            return result
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
        SELECT source,
            CONVERT(DATE_FORMAT(ts, %s), SIGNED) AS day, 
            MONTH(ts) as month, 
            YEAR(ts) as year, 
            HOUR(ts) as hour, 
            AVG(value) as value
        FROM `main` 
        WHERE param=%s 
        GROUP BY source, year, month,day,hour 
        ORDER BY source, year,month, day,hour  
        """,['%d',param])
        result = [models.HourAverageValue(*row) for row in cs.fetchall()]
        return result