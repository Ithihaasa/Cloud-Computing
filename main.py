from flask import Flask, redirect, flash, request, make_response, abort, render_template, url_for
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from werkzeug.utils import secure_filename
import json
import os

UPLOAD_FOLDER = '/files/'
ALLOWED_EXTENSIONS = {'txt'}
global result

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db_connect = create_engine('sqlite:///cc.db')


@app.route("/", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        payload = request.form
        connection = db_connect.connect()
        connection.execute("insert into user_details(first_name,last_name,email, password) values(?,?,?,?)",
                           (payload['first_name'], payload['last_name'], payload['email'], payload['password']))
        return redirect(url_for("login"))
    return render_template("test.html")


@app.route('/login', methods=['GET', "POST"])
def login():
    if request.method == 'POST':
        global result
        payload = request.form
        email = payload['email']
        password = payload['password']
        connection = db_connect.connect()
        query = connection.execute(
            "select * from user_details where email = ?", email)
        records = query.cursor.fetchall()
        if records[0][-1] == password:
            query = connection.execute(
                "select first_name, last_name,email from user_details where email = ?", email)
            result = query.cursor.fetchall()
            return redirect(url_for("display", result=result))
        else:
            return "Username or password is incorrect"

    return render_template('login.html')


@app.route("/display", methods=['GET', 'POST'])
def display():
    global result
    if request.method == "POST":
        global result
        data = request.files['file']
        data = data.read()
        content = str(data, 'utf-8').split()
        dict_ = dict()
        for con in content:
            if con not in dict_:
                dict_[con] = 1
            else:
                dict_[con] += 1
        total_words = sum(dict_.values())
        return render_template("display_info.html", result=result, data=dict_, total_words=total_words)
    return render_template("display.html", result=result)


@app.route("/display_info", methods=['GET', 'POST'])
def display_files_info():
    global result
    return render_template("display_info.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
