import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "task_manager"
app.config["MONGO_URI"] = "mongodb+srv://root:Dublin15@mycluster-sw86k.mongodb.net/task_manager?retryWrites=true&w=majority"


mongo = PyMongo(app)

@app.route("/")
def hello():
    return "<h1 style='color:blue;text-align:center;'>Hello World</h1>"

# get tasks route
@app.route("/get_tasks")
def get_tasks():
    return render_template("tasks.html", tasks= mongo.db.tasks.find())


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)
