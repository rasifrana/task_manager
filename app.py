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
    return "<h1 style='color:blue;text-align:center;'>Hellooo World</h1>"

# get tasks route
@app.route("/get_tasks")
def get_tasks():
    return render_template("tasks.html", tasks= mongo.db.tasks.find())

# Add task route
@app.route("/add_task")
def add_task():
    return render_template("addtask.html", catagories= mongo.db.catagories.find())


# Post a task on url
@app.route("/insert_task", methods=["POST"])
def insert_task():
    tasks = mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for("get_tasks"))


@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task = mongo.db.tasks.find_one({"_id:": ObjectId(task_id)})
    all_catagories = mongo.db.catagories.find()
    return render_template("edittask.html", task= the_task, catagories = all_catagories)

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)
