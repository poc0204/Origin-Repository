import mysql.connector
import json
import re
connection = mysql.connector.connect(
        host = 'localhost',
        database = 'website',
        user = 'root',
        password = 'mysql'
)
cursor = connection.cursor()
sql = "select  COUNT(id) from level2; "
cursor.execute(sql)
id_count = cursor.fetchall()
page_start = int(input())
page_max = id_count[0][0]/12
json_data = []

data_images =[]
if page_start <= page_max:
    page_start_time = page_start*12
    sql = "select * from level2 LIMIT {}, 12; ".format(page_start_time)
    cursor.execute(sql)
    id_data = cursor.fetchall()
    for i in range(len(id_data)):
        data_images =[]
        sql = "select images from level2_images where id_images = '{}'".format(id_data[i][0])
        cursor.execute(sql)
        #id_images = cursor.fetchall()

        id_images = cursor.fetchall()
        for j in range(len(id_images)):
            images = str(id_images[j])
            images = re.sub(r'[(,)]','',images)
            images = re.sub(r' ',',',images)
            images = re.sub(r'\'','',images)
            data_images.append(images)
        #print(data_images)        
        data={
                "nextPage": page_start+1,
                "data": {
                    "id":id_data[i][0],
                    "name":id_data[i][1],
                    "category":id_data[i][6],
                    "description":id_data[i][2],
                    "address":id_data[i][3],
                    "transport":id_data[i][4],
                    "mrt":id_data[i][5],
                    "latitude":id_data[i][7],
                    "longitude":id_data[i][8],
                    "images":data_images
                }

            }
        
        json_data.append(data)
    print(json_data[0])


else:
    print('超出頁面')

# sql = "select id from level2 LIMIT '{}','{}'; ".format(page_start,page_end)
