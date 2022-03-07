from datetime import date
import mysql.connector

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
data = []
for_id = []
for_name = []
for_category = []
for_description = []
for_address = []
for_transport = []
for_mrt = []
for_latitude = []
for_longitude = []
for_images =[]

if page_start <= page_max:
    page_start_time = page_start*12
    sql = "select * from level2 LIMIT {}, 12; ".format(page_start_time)
    cursor.execute(sql)
    id_data = cursor.fetchall()
    for i in range(len(id_data)):
        for_id.append(id_data[i][0])
        for_name.append(id_data[i][1])
        for_category.append(id_data[i][6])
        for_description.append(id_data[i][2])
        for_address.append(id_data[i][3])
        for_transport.append(id_data[i][4])
        for_mrt.append(id_data[i][5])
        for_latitude.append(id_data[i][7])
        for_longitude.append(id_data[i][8])
        sql = "select images from level2_images where id_images = '{}'".format(id_data[i][0])
        cursor.execute(sql)
        id_images = cursor.fetchall()
      
        for_images.append(id_images)
    data.append(
            [{
            "nextPage": page_start+1,
            "data": [{
                "id":for_id,
                "name":for_name,
                "category":for_category,
                "description":for_description,
                "address":for_address,
                "transport":for_transport,
                "mrt":for_mrt,
                "latitude":for_latitude,
                "longitude":for_latitude,
                "images":for_images
            }]

                }])
            
    print(data[0][0]['data'][0]['images'][1])
else:
    print('超出頁面')

# sql = "select id from level2 LIMIT '{}','{}'; ".format(page_start,page_end)
