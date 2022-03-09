from email import header
from encodings.utf_8_sig import encode
from this import d
from urllib import response
from flask import Flask ,redirect,url_for ,render_template , request , session  , make_response,jsonify
import math
import json , re
from operator import le
from telnetlib import PRAGMA_HEARTBEAT
from matplotlib.font_manager import json_dump
import mysql.connector
from mysql.connector import Error
from numpy import False_

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

# Pages
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")


@app.route("/api/attractions",methods=['GET'])
def api_attractions():
	page = request.args.get('page')
	keyword = request.args.get('keyword')
	connection = link_mysql() 
	cursor = connection.cursor()

	sql = "select  COUNT(id) from level2; "
	cursor.execute(sql)
	id_count = cursor.fetchall()
	
	page_start = int(page)
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
		if keyword != None:
			sql = "select * from level2 where name LIKE '%{}%'; ".format(keyword)
			if page != None:
				sql = "select  COUNT(id) from level2 where name LIKE '%{}%'; ".format(keyword); 
				cursor.execute(sql)
				id_count = cursor.fetchall()
				page_start = int(page)
				page_max = id_count[0][0]/12
				if page_start <= page_max:
					page_start_time = page_start*12
					sql = "select * from level2 where name LIKE '%{}%' LIMIT {}, 12; ".format(keyword,page_start_time)
				else:
					msg = "超出頁面"
					data = {
					"message":msg
					}
					data = json.dumps(data,ensure_ascii=False).encode('utf8')
					return data
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
		data = json.dumps(data,ensure_ascii=False).encode('utf8')
		return data
	else:
		msg = "伺服器內部錯誤"
		data = {
		"error":link_mysql()  == False,
		"message":msg
		}
		data = json.dumps(data,ensure_ascii=False).encode('utf8')
		res = make_response(data)
		res.status='500'
		return res 

@app.route("/api/attractions/<id>",methods=['GET'])
def api_attraction(id):
	try:
		connection = link_mysql() 
		cursor = connection.cursor()
		sql = "select * from level2 where id = '{}'".format(id)
		cursor.execute(sql)
		id_data = cursor.fetchall()
		sql = "select * from level2_images where id_images = '{}'".format(id)
		cursor.execute(sql)
		id_images = cursor.fetchall()
		data_images = []
		if id_data != []:
			for i in range(len(id_images)):
				data_images.append(id_images[i][1])
			
			data = {
				'data':{
				"id": id_data[0][0],
				"name":id_data[0][1] ,
				"category": id_data[0][6],
				"description": id_data[0][2],
				"address": id_data[0][3],
				"transport": id_data[0][4],
				"mrt": id_data[0][5],
				"latitude": id_data[0][7],
				"longitude": id_data[0][8],	
				"images":data_images
				}
				}
			data = json.dumps(data,ensure_ascii=False).encode('utf8')
			return data 
		else:
			msg = "景點編號不正確"
			data = {
			"error":id_data == [] ,
			"message":msg
			
			}
			data = json.dumps(data,ensure_ascii=False).encode('utf8')
			res = make_response(data)
			res.status='400'
			return res 

	except:
		msg = "伺服器內部錯誤"
		data = {
		"error":link_mysql()  == False,
		"message":msg
		}
		data = json.dumps(data,ensure_ascii=False).encode('utf8')
		res = make_response(data)
		res.status='500'
		return res 

@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

def link_mysql():
    try:
        connection = mysql.connector.connect(
            host = 'localhost',
            database = 'website',
            user = 'root',
            password = 'mysql'
        )
    	
    except:
       return False
   
    return connection  



app.run(host='0.0.0.0',port=3000)