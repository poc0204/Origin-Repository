import json , re
from operator import le
from telnetlib import PRAGMA_HEARTBEAT
from matplotlib import image
import mysql.connector
from mysql.connector import Error

with open("taipei-attractions.json","r" , encoding="utf8" ) as f:
    data = json.load(f)

all_data = data['result']['results']

connection = mysql.connector.connect(
    host = 'localhost',
    database = 'website',
    user = 'root',
    password = 'mysql'
)
cursor = connection.cursor()


set_data = []
for show in all_data:
    id = int(show['_id'])
    name = show['stitle']
    description = show['xbody']
    address = show['address']
    transport = show['info']
    mrt = show['MRT']
    latitude = show['latitude']
    longitude = show['longitude']
    category = show['CAT2']
    sql = " insert into level2 (id ,name ,description ,address ,transport ,mrt ,latitude ,longitude ,category) values ('{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(id,name,description,address,transport,mrt,latitude,longitude,category)
    cursor.execute(sql)
    connection.commit()  

    all_img = []
    for j in range(len(all_data)):
        all_http = re.finditer(r'http',all_data[j]['file'],flags = re.M)
        all_jpg = re.finditer(r'(?i)jpg',all_data[j]['file'], flags = re.M)
        index_http = []
        index_jpg = []

    for matchhttp in all_http:
        index_http.append(matchhttp.span()[0])
    for matchjpg in all_jpg:
        index_jpg.append(matchjpg.span()[1])

    for i in range(len(index_http)):
        images = all_data[j]['file'][index_http[i]:index_jpg[i]]
        sql = " insert into level2_images (id_images ,images) values ('{}','{}');".format(id,images)
        cursor.execute(sql)
        connection.commit()  

   
    # data={
    #     'id':show['_id'], 
    #     "name": show['stitle'],
    #     "category": show['CAT2'],
    #     "description": show['xbody'], 
    #     "address": show['address'], 
    #     "transport": show['info'],
    #     "mrt": show['MRT'],
    #     "latitude":show['latitude'],
    #     "longitude": show['longitude'],
    #     "images": all_img
    # }
    # all_img = ""
    # set_data.append(data)


# for i in range(len(set_data)):
#     id = int(show['_id'])
#     name = show['stitle']
#     description = show['xbody']
#     address = show['address']
#     transport = show['info']
#     mrt = show['MRT']
#     latitude = show['latitude']
#     longitude = show['longitude']
#     images =set_data[0]['images']
#     category = show['CAT2']
#     sql = " insert into level2 (id ,name ,description ,address ,transport ,mrt ,latitude ,longitude ,category) values ('{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(id,name,description,address,transport,mrt,latitude,longitude,category)
#     cursor.execute(sql)
#     connection.commit()



# for show in all_data:
#     id = int(show['_id'])
#     name = show['stitle']
#     description = show['xbody']
#     address = show['address']
#     transport = show['info']
#     mrt = show['MRT']
#     latitude = show['latitude']
#     longitude = show['longitude']
#     images =set_data[0]['images']
#     category = show['CAT2']
#     sql = " insert into level2 (id ,name ,description ,address ,transport ,mrt ,latitude ,longitude ,category) values ('{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(id,name,description,address,transport,mrt,latitude,longitude,category)
#     cursor.execute(sql)
#     connection.commit()
#     print(len(show))

cursor.close()
connection.close()    
