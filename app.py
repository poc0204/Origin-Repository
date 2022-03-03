from flask import Flask ,redirect,url_for ,render_template , request , session 
import json , re
from operator import le
from telnetlib import PRAGMA_HEARTBEAT
import mysql.connector
from mysql.connector import Error

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

# Pages
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/attraction/<id>", methods=['GET'])
def attraction(id):
	print('id:',id)
	connection = link_mysql() 
	cursor = connection.cursor()
	sql = " select * from level2 inner join level2_images on id = id_images where id= '{}' ".format(id)
	cursor.execute(sql)
	id_data = cursor.fetchall()
	print(range(len(id_data)))
	return render_template("attraction.html")

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
        
    except Error as e:
        print('database error :',e)
    return connection

app.run(port=3000)