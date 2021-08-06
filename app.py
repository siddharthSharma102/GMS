from flask import Flask, request, redirect, url_for, render_template, flash, session
from flask_pymongo import PyMongo
import pymongo
import os
import twilio
from twilio.rest import Client


app = Flask(__name__)
acc_sid = "AC6b0ad0de3680fb40ef91442c71e5e10e"
auth_token = "6b0fd4a1479a00d00cdc7586f78caf63"
client = Client(acc_sid, auth_token)
mongo_connect_url = "mongodb+srv://gms_user:12345@gms.mn0q8.mongodb.net/test"
cluster = pymongo.MongoClient(mongo_connect_url)
app.config["MONGO_URI"] = mongo_connect_url
mongo = PyMongo(app)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/signup")
def signup():
    return render_template('signup.html')
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/gms/login", methods =["GET", "POST"])
def login():
    global cluster

    error = None
    if request.method == "POST":
        uname = request.form["uname"]
        print(uname)
        pwd = request.form["pwd"]
        print(pwd)
        db = cluster["gms"]
        collection = db["login"]

        users = mongo.db.login
        login_user = collection.find_one({'username': uname})
        print(login_user)
        if login_user:
            if login_user['password'] == pwd:
                return redirect(url_for('.profile', uname=uname, pwd=pwd))
            else:
                 error = "Invalid Credentials"
        else:
             error = "Invalid Credentials"
    return render_template("login.html", error=error)

@app.route('/gms/user/add_bin')
def bin():
    return render_template('add_bin.html')

def validate():
    pass

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/gms/user/profile")
def profile():
    uname = request.args['uname']
    pwd = request.args['pwd']
    print(uname, pwd)
    return render_template("profile.html", uname=uname)

@app.route("/gms/add_bin/")
def add_bin():
    return render_template("add_bin.html")

@app.route("/gms/user/edit_profile")
def edit_profile():
    return render_template("edit_profile.html")

@app.route("/gms/total_bins")
def tot_bins():
    return render_template("total_bins.html")

@app.route("/gms/total_bins_1", methods=["POST"])
def send():
    global client
    block = request.form["block"]
    street = request.form["street"]
    district = request.form["district"]
    state = request.form["state"]
    pin = request.form["pin"]
    arr = [block, street, district, state, pin]
    print(arr)
    message = ",".join(arr)
    
    
    return render_template("total_bins.html",message=message )




app.run(debug=True)