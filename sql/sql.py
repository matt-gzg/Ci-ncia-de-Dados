import mysql.connector

cnx = mysql.connector.connect(
    user='matt',
    password='Matt@2006!',
    host='127.0.0.1',
    database='teste'
)

cnx.close()