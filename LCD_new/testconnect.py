import pymysql

conn = pymysql.connect(host = '172.30.1.6', user='root', password='raspberry', db='TEMPERATURE', charset='utf8')

cursor = conn.cursor()

sql = "INSERT INTO server_room (date, time, temperature, humidity) VALUES (%s, %s, %s, %s)"

cursor.execute(sql, ("2021-01-31", "02:55:01", "4", "5"))
conn.commit()
conn.close()