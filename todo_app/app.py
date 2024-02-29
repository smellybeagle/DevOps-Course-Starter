from todo_app.view_model import ViewModel
from .data.item import Item
from .flask_config import Config
import os
from flask import Flask, redirect, render_template, request
import pymongo
from bson import ObjectId # For ObjectId to work



def create_app():
    dbconnection = os.getenv("MONGODB_CONN")
    client = pymongo.MongoClient(dbconnection)   
    db = client.todo_app    
    collection = db.todolist
    
    app = Flask(__name__)
    app.config.from_object(Config())
    
    
    def todolists():
        dicttodo=collection.find({"Status" : "To Do"})
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
    
    @app.route('/')
    def index():
        todo_items = todolists()
        doing_items = doinglists()
        done_item = donelists()
        item_view_model = ViewModel(todo_items, doing_items, done_item)
        return render_template('index.html', view_model = item_view_model)
    
    @app.route('/additem', methods = ["POST"])
    def add_new_item():
        name=request.values.get("name")
        desc=request.values.get("desc")
        collection.insert_one({ "name":name, "desc":desc, "Status": "To Do"})
        return redirect('/')   

    @app.route('/movedoing', methods = ["POST"])
    def movedoing():
        id=request.values.get("_id")
        collection.find({"_id":ObjectId(id)})
        collection.update_one({"_id":ObjectId(id)}, {"$set": {"Status":"In Progress"}})
        return redirect('/')
    

    @app.route('/movedone', methods = ["POST"])
    def movedone():
        id=request.values.get("_id")
        collection.find({"_id":ObjectId(id)})
        collection.update_one({"_id":ObjectId(id)}, {"$set": {"Status":"Completed"}})
        return redirect('/')

    @app.route('/delete', methods = ["POST"])
    def remove():
        id=request.values.get("_id")
        collection.find({"_id":ObjectId(id)})
        collection.delete_one({"_id":ObjectId(id)})
        return redirect('/')

    return app

if __name__ == '__main__':
    app = create_app()