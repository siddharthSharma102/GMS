from flask import Flask, request, redirect, url_for, render_template, flash, session
from flask_pymongo import PyMongo
import pymongo

app = Flask(__name__)
mongo_connect_url = "mongodb+srv://gms_user:gms121@gms.mn0q8.mongodb.net/test"
cluster = pymongo.MongoClient(mongo_connect_url)
app.config["MONGO_URI"] = mongo_connect_url
mongo = PyMongo(app)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/gms/login", methods =["GET", "POST"])
def login():
    global cluster

    error = None
    if request.method == "POST":
        uname = request.form["uname"]
        pwd = request.form["pwd"]
        
        db = cluster["gms"]
        collection = db["login"]

        users = mongo.db.login
        login_user = collection.find_one({'username': uname})
        print(login_user)
        if login_user:
            if login_user['password'] == pwd:
                return redirect(url_for('profile'))
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
    return render_template("profile.html")

@app.route("/gms/add_bin/")
def add_bin():
    return render_template("add_bin.html")

@app.route("/gms/user/edit_profile")
def edit_profile():
    return render_template("edit_profile.html")

@app.route("/gms/total_bins")
def tot_bins():
    return render_template("total_bins.html")

@app.route("/gms/track/bin")
def bin_track():
    return render_template("bin_track_map.html")
app.run(debug=True)