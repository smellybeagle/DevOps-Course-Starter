import os
from flask import redirect, request
from todo_app.debugger import writelog
from todo_app.data.item import Item
import pymongo
from bson.objectid import ObjectId # For ObjectId to work


mongodb_host = os.environ.get('MONGO_HOST', 'localhost')
mongodb_port = int(os.environ.get('MONGO_PORT', '27017'))

#Configure the connection to the database
client = pymongo.MongoClient(mongodb_host, mongodb_port) 
#Select the database   
db = client.todo_app    
#Select the collection
collection = db.todolist



def init_mongodb():

    def todolists():
        dicttodo=list(collection.find({"Status" : "To Do"}))
        todos = []
        for todo_item in dicttodo:
            todos.append(Item.from_mongo(todo_item))
            return todos

    def doinglists():
            dictdoing=collection.find({"Status" : "In Progress"})
            doing = []
            for doing_item in dictdoing:
                doing.append(Item.from_mongo(doing_item))
                return doing
        
    def donelists():
        dictdone=collection.find({"Status" : "Completed"})
        done = []
        for done_item in dictdone:
            done.append(Item.from_mongo(done_item))
            return done


headers = {"Accept": "application/json"}


#def add_new_item():
#        name=request.values.get("name")
#        desc=request.values.get("desc")
#        collection.insert_one({ "name":name, "desc":desc, "Status": "To Do"})
#        return redirect('/')


#@app.route('/movedoing', methods = ["POST"])
#def movedoing():
#        id=request.values.get("_id")
#        collection.update_one({"_id"}, {'$set':{ "Status": "In Progress"}})
#        return redirect('/')
    

#@app.route('/movedoing', methods = ["POST"])
#def movedone():
#        id=request.values.get("_id")
#        collection.update_one({"_id"}, {'$set':{ "Status": "Completed"}})
#        return redirect('/')