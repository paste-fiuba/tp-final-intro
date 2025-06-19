import pymysql
import config

def get_connection():
    return pymysql.connect(
        **config.DB_CONFIG,
        cursorclass=pymysql.cursors.DictCursor,
    )

