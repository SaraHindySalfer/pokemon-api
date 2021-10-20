import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="1234",
    db="sql_intro",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)
host = '127.0.0.1'
port = 3000
