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
            SELECT source, hour, AVG(value) as value
            FROM (
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
            ) group_date
            GROUP BY source, hour
            """,['%d',param])
            result = [models.HourAverageValue(*row) for row in cs.fetchall()]
            return result
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
        SELECT source, hour, AVG(value) as value
        FROM (
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
        ) group_date
        GROUP BY source, hour
        """,['%d',param])
        result = [models.HourAverageValue(*row) for row in cs.fetchall()]
        return result
    
def hour_average_value_by_source(param, source):
    if param == 'humcount':
        with pool.connection() as conn, conn.cursor() as cs:
            cs.execute("""
            SELECT source, hour, AVG(value) as value
            FROM (
            SELECT source,
                CONVERT(DATE_FORMAT(ts, %s), SIGNED) AS day, 
                MONTH(ts) as month, 
                YEAR(ts) as year, 
                HOUR(ts) as hour, 
                SUM(value) as value
            FROM `main` 
            WHERE param=%s and source=%s
            GROUP BY source, year, month,day,hour 
            ORDER BY source, year,month, day,hour  
            ) group_date
            GROUP BY source, hour
            """,['%d',param, source])
            result = [models.HourAverageValue(*row) for row in cs.fetchall()]
            return result
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
        SELECT source, hour, AVG(value) as value
        FROM (
        SELECT source,
            CONVERT(DATE_FORMAT(ts, %s), SIGNED) AS day, 
            MONTH(ts) as month, 
            YEAR(ts) as year, 
            HOUR(ts) as hour, 
            AVG(value) as value
        FROM `main` 
        WHERE param=%s and source=%s
        GROUP BY source, year,month,day,hour 
        ORDER BY source, year,month, day,hour  
        ) group_date
        GROUP BY source, hour
        """,['%d',param, source])
        result = [models.HourAverageValue(*row) for row in cs.fetchall()]
        return result
    
def compare_between_humcount_and_value(param):
    with pool.connection() as conn, conn.cursor() as cs:
            cs.execute("""
            SELECT group_param.year,group_param.month,group_param.day,group_param.hour, AVG(group_hum.value) as humcount, AVG(group_param.value) as comparevalue
            FROM (
            SELECT CONVERT(DATE_FORMAT(ts, %s), SIGNED) AS day, MONTH(ts) as month, YEAR(ts) as year, HOUR(ts) as hour, SUM(value) as value
            FROM `main` 
            WHERE param="humcount"
            GROUP BY year,month,day,hour 
            ORDER BY year,month, day,hour  
            ) group_hum,
            (
            SELECT CONVERT(DATE_FORMAT(ts, %s), SIGNED) AS day, MONTH(ts) as month, YEAR(ts) as year, HOUR(ts) as hour, AVG(value) as value
            FROM `main` 
            WHERE param=%s
            GROUP BY year,month,day,hour 
            ORDER BY year,month, day,hour  
            ) group_param
            WHERE (group_hum.hour = group_param.hour) and (group_hum.day = group_param.day) and (group_hum.month = group_param.month) and (group_hum.year = group_param.year)
            GROUP BY year,month,day,hour 
            """,['%d','%d', param])
            result = [models.CompareValue(*row) for row in cs.fetchall()]
            return result