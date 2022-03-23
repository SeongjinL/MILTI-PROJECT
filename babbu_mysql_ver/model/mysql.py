import pymysql

MYSQL_HOST = 'localhost'
MYSQL_CONN = pymysql.connect(
    host=MYSQL_HOST,
    port=3306,
    user='lab05',
    passwd='lab05',
    db='test123',
    charset='utf8'
)


def conn_mysqldb():
    if not MYSQL_CONN.open:
        MYSQL_CONN.ping(reconnect=True)
    return MYSQL_CONN
