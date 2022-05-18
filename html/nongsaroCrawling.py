import pymysql
plant = []
temp = []
hum = []

def selectPlant():
    conn = pymysql.connect(host = '192.168.86.91', user='root', password='raspberry', db='TEMPERATURE', charset='utf8')

    plant = []

    cursor = conn.cursor()

    sql = "SELECT plant from nongsaro"

    cursor.execute(sql)
    datas = cursor.fetchall()
    for data in datas:
        plant.append(data[0])
    conn.commit()
    conn.close()
    
    return plant


def search(pName):
    ##
    conn = pymysql.connect(host = '192.168.86.91', user='root', password='raspberry', db='TEMPERATURE', charset='utf8')
    cursor = conn.cursor()
    ##
    temp = []
    hum = []

    sql2 = "SELECT temp, humi from nongsaro where plant = " + "\'" + pName + "\'"
    cursor.execute(sql2)
    datas = cursor.fetchall()
    for data in datas:
        temp.append(data[0])
        hum.append(data[1])    
    conn.commit()
    conn.close()
    return temp, hum

# print(selectPlant())
print(search('후피향나무')[0][0])

