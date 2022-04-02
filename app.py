from datetime import date
from pickle import NONE
from pprint import pprint
from telnetlib import PRAGMA_HEARTBEAT
from urllib import response
from wsgiref.util import request_uri
from flask import Flask ,redirect,url_for ,render_template , request , session  , make_response,jsonify
import json , re
import mysql.connector
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['SECRET_KEY'] = "usertest"
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


@app.route("/api/user",methods = ['GET', 'POST', 'PATCH', 'DELETE'])
def api_user():
	if request.method == 'GET':
		id = session.get('id')
		name = session.get('name')
		email = session.get('email')
	
		return jsonify({"data":{"id":id,"name":name,"email":email}}),200

	if request.method == 'PATCH':
		print('PATCH')
		data = json.loads(request.data)
		member_email = data['email']
		member_password = data['password']
		try:
			connection = link_mysql()
			cursor = connection.cursor()
		except:
			return jsonify({"error":True ,"message": "伺服器內部錯誤"}) , 500
		sql = " select * from level2member where email = '{}' ; ".format(member_email)
		cursor.execute(sql)
		all_email = cursor.fetchall()
		
		cursor.close()
		connection.close()
		if all_email == [] or all_email[0][3] != member_password :
			error_message = "信箱、密碼輸入錯誤"
			return jsonify({'error':True,"message":error_message}) ,400


		session["id"] = all_email[0][0]
		session["name"] = all_email[0][1]
		session["email"] = all_email[0][2]

	
		return jsonify({"ok": all_email[0][3] == member_password})

	if request.method == 'POST':
		print('POST')
		data = json.loads(request.data)
		member_email = data['email']
		member_password = data['password']
		member_name = data['name']

		try:
			connection = link_mysql()
			cursor = connection.cursor()
		except:
			return jsonify({"error":True ,"message": "伺服器內部錯誤"}) , 500

		sql = " select email from level2member where email = '{}' ; ".format(member_email)
		cursor.execute(sql)
		all_email = cursor.fetchall()
		if all_email == []:
			sql = " insert into level2member (name ,email ,password) values ('{}' ,'{}' ,'{}');".format(member_name,member_email,member_password)
			cursor.execute(sql)
			connection.commit()
			cursor.close()
			connection.close()    
			return jsonify({"ok":True})
		
		error_message = "帳號已經被註冊"
		return jsonify({"error":True,"message":"註冊失敗，重複的Email"}) , 400
	if request.method == 'DELETE':
		session.clear()
		return jsonify({"ok":True}),200

@app.route("/booking")
def booking():
	return render_template("booking.html")

@app.route("/api/booking" , methods = ['GET', 'POST', 'DELETE'])
def api_booking():
	if request.method == 'GET':
		id = session.get('id')
		attraction_id = session.get('attraction_id')
		attraction_name = session.get('attraction_name')
		attractiona_address = session.get('attractiona_address')
		attraction_image = session.get('attraction_image')
		date = session.get('date')
		time = session.get('time')
		price = session.get('price')
		name = session.get('name')
		email = session.get('email')
		if attraction_id == None:
			return jsonify({"data":None}) , 200
		if id == None:
			return jsonify({"error": True,"message": "未登入系統，拒絕存取"}) , 403
		else:
			return jsonify({
				"data": {
				"attraction": {
				"id": attraction_id,
				"name": attraction_name,
				"address": attractiona_address,
				"image": attraction_image
				},
				"date": date,
				"time": time,
				"price": price,
				"member":name,
				"email":email
				}}) , 200
	if request.method == 'POST':
		try:
			connection = link_mysql()
			cursor = connection.cursor()
		except:
			return jsonify({"error": True,"message": "伺服器內部錯誤"}) , 500
		data = json.loads(request.data)
		if data['attractionId'] == '' or data['date'] == '' or data['time'] == '' or data['price'] == '' :
			return jsonify({"error": True,"message": "建立失敗，輸入不正確或其他原因"}) , 400
	
		name = session.get('name')
		if name == None :
			return jsonify({"error": True,"message": "未登入系統，拒絕存取"}) , 403
		else:
			session["attraction_id"] = data['attractionId']
			session["attraction_name"] = data['name']
			session["attractiona_address"] = data['address']
			session["attraction_image"] = data['image']
			session["date"] = data['date']
			session["time"] = data['time']
			session["price"] = data['price']
			return jsonify({"ok": True}) , 200
	if request.method == 'DELETE':
		id = session.get('id')
		if id == '':
			return jsonify({"error":True,"message": "未登入系統，拒絕存取"}) , 403
		session["attraction_id"] = ''
		session["attraction_name"] = ''
		session["attractiona_address"] = ''
		session["attraction_image"] = ''
		session["date"] =''
		session["time"] = ''
		session["price"] = ''
		return jsonify({"ok":True}) , 200
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
