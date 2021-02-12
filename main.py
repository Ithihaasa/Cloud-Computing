from flask import Flask, jsonify, request, make_response, abort, render_template
from flask_restful import Resource, Api
from sqlalchemy import create_engine
import json

app = Flask(__name__)
api = Api(app)

db_connect = create_engine('sqlite:///cc.db')

@app.route("/", methods=['GET','POST'])
def register():
    if request.method == "POST":
        payload = request.form
        connection = db_connect.connect()
        connection.execute("insert into user_details(first_name,last_name,email, password) values(?,?,?,?)", (payload['first_name'],payload['last_name'],payload['email'], payload['password']))
        return render_template('login.html')
    return render_template("test.html")


@app.route('/login', methods = ['GET', "POST"])
def login():
    if request.method == 'POST':
        payload = request.form
        email = payload['email']
        password = payload['password']
        connection = db_connect.connect()
        query = connection.execute("select * from user_details where email = ?", email)
        records = query.cursor.fetchall()
        if records[0][-1] == password:

            # query = connection.execute("select first_name, last_name,email from user_details where email = ?", email)
            # result = query.cursor.fetchall()
            # return render_template("display.html", result= result)
            return email
        else:
            return "Username or password is incorrect"

    # return render_template('login.html')


@app.route("/display", methods = ['GET', 'POST'])
def display():
    email = login()
    # file_ = request.files['Files']
    # print(file_)
    query = connection.execute("select first_name, last_name,email from user_details where email = ?", email)
    result = query.cursor.fetchall()
    return render_template("display.html", result = result)
    # connection = db_connect.connect()
    # query = connection.execute("select first_name, last_name,email from user_details where email = ?", email)
    # return {}

if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0')

