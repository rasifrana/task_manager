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

# get Add task route
@app.route("/add_task")
def add_task():
    return render_template("addtask.html", catagories= mongo.db.catagories.find())


# insert task / Post a task on url
@app.route("/insert_task", methods=["POST"])
def insert_task():
    tasks = mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for("get_tasks"))


# Edit a Taks page
@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    all_catagories = mongo.db.catagories.find()
    return render_template("edittask.html", task= the_task, catagories = all_catagories)


# Update task route
@app.route("/update_task/<task_id>", methods=["POST"])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update( {'_id': ObjectId(task_id)},
    {
        'task_name':request.form.get('task_name'),
        'category_name':request.form.get('category_name'),
        'task_description': request.form.get('task_description'),
        'due_date': request.form.get('due_date'),
        'is_urgent':request.form.get('is_urgent')
    })
    return redirect(url_for("get_tasks"))


# Delete a task
@app.route("/delete_task/<task_id>")
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for("get_tasks"))

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)
