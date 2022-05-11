from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
app = Flask(__name__)

#client = MongoClient('mongodb://mongo:27017/')
#Note that the hostname in the MONGO_URI Flask configuration variable is
#  defined as ‘mongo’ instead of ‘localhost’. This is because 
# ‘mongo’ will be the name of our database container, and containers
# in the same Docker network can talk to each other by their names. To run
#locally change mongo to localhost
app.config["MONGO_URI"] = "mongodb://mongo:27017/dev"
mongo = PyMongo(app)
db = mongo.db
#db = client.db    
todos = db.todos

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todos.insert_one({'title':title, 'desc':desc})
        print(request.form)
        return redirect(url_for('home'))
    all_todos = todos.find()
    return render_template('index.html', todos=all_todos, t= todos)

@app.route('/<id>/delete/', methods=['GET', 'POST'])
def delete(id):
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('home'))

@app.route('/<id>/update',methods=['GET','POST'])
def update(id):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todos.update_one({"_id": ObjectId(id)},{"$set":{ "title":title, "desc":desc}}, True)
        print(request.form)
        return redirect(url_for("home"))
    todo= todos.find_one({"_id": ObjectId(id)})
    return render_template('update.html', todo=todo)

# print(todos.find({"_id": ObjectId('624d4c8835a8d097fb6c5da8')}))
    

if __name__ == "__main__": 
    app.run(host= '0.0.0.0', port=5000, debug=True)
