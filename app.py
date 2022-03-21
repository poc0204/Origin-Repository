from datetime import date
from pprint import pprint
from urllib import response
from wsgiref.util import request_uri
from flask import Flask ,redirect,url_for ,render_template , request , session  , make_response,jsonify
import json , re
import mysql.connector
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
	print('page',page)
	if page == None:
		page = 0
	keyword = request.args.get('keyword')
	connection = link_mysql() 	
	cursor = connection.cursor()
	sql = "select  COUNT(id) from level2; "
	cursor.execute(sql)
	id_count = cursor.fetchall()
	page_start = int(page)
	page_max = id_count[0][0]/12
	json_data = []

	if page_start <= page_max: 
		page_start_time = page_start*12
		sql = "select * from level2 LIMIT {}, 13; ".format(page_start_time)
		if keyword != None:
			sql = "select * from level2 where name LIKE '%{}%'; ".format(keyword)
			
			print(keyword)
			if page_start <= page_max:
				page_start_time = page_start*12
				sql = "select * from level2 where name LIKE '%{}%' LIMIT {}, 13; ".format(keyword,page_start_time)
			else:
				msg = "超出頁面"
				data = {
				"message":msg
				}
				return jsonify({'data':data})
		cursor.execute(sql)
		id_data = cursor.fetchall()
		if id_data !=[]:
			for i in range(len(id_data)):
				data_images =[]
				sql = "select images from level2_images where id_images = '{}'".format(id_data[i][0])
				cursor.execute(sql)
				id_images = cursor.fetchall()
				for j in range(len(id_images)):
					images = str(id_images[j])
					images = re.sub(r'[(,)]','',images)
					images = re.sub(r' ',',',images)
					images = re.sub(r'\'','',images)
					data_images.append(images)
				data={
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

					
				json_data.append(data)
			
			return jsonify({"nexypage":page_start+1,"data":json_data})
		else:
			msg = "無此景點，請重新輸入"
			data = {
			"error":True,
			"message":msg
			}
			return jsonify({'data':data}) 
	else:
			msg = "超出頁面"
			data = {
			"error":True,
			"message":msg
			}
			return jsonify({'data':data}) 


@app.route("/api/attractions/<id>",methods=['GET'])
def api_attraction(id):
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
	
	
		return jsonify({'data':data})
	else:
		msg = "景點編號不正確"
		data = {
		"error":id_data == [] ,
		"message":msg
		
		}

		return jsonify({'data':data}) ,400


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
			user = 'newuser',
			password = 'newpassword'
		)
		
	except:
		msg = "伺服器內部錯誤"
		data = {
		"error":True,
		"message":msg
		}

		return jsonify({'data':data}) ,500 

	else:
		return connection
 
		

	
   



app.run(host='0.0.0.0',port=3000)
