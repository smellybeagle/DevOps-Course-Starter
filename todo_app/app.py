from todo_app.view_model import ViewModel
from .data.item import Item
from .flask_config import Config
import os
from flask import Flask, redirect, render_template, request, url_for,session
import pymongo
from bson import ObjectId # For ObjectId to work
from todo_app.oauth import blueprint
from flask_dance.contrib.github import github
from werkzeug.middleware.proxy_fix import ProxyFix
from todo_app.logging import writelog,logtoconsole
from loggly.handlers import HTTPSHandler
from logging import Formatter



def create_app():
    logtoconsole()
    
    dbconnection = os.getenv("MONGODB_CONN")
    client = pymongo.MongoClient(dbconnection)   
    db = client.todo_app    
    collection = db.todolist
    
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config.from_object(Config())
    app.register_blueprint(blueprint, url_prefix="/login")
      
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
        if not github.authorized:   
            return redirect(url_for("github.login"))
        todo_items = todolists()
        doing_items = doinglists()
        done_item = donelists()
        item_view_model = ViewModel(todo_items, doing_items, done_item)
        username=session["username"]
        role = session["role"]
#        context='index'
#        function = 'login'
#        datastring = username
        app.logger.info('%s logged in successfully', username)
        #writelog(context, function, 'datastring',datastring)
        return render_template('index.html', view_model = item_view_model,username=username,role=role)
    
    @app.route('/additem', methods = ["POST"])
    def add_new_item():
        if not github.authorized:
            return redirect(url_for("github.login"))
        name=request.values.get("name")
        desc=request.values.get("desc")
        collection.insert_one({ "name":name, "desc":desc, "Status": "To Do"})
        app.logger.debug({ "name":name, "desc":desc, "Status": "To Do"})
        context = 'app.py add-new-item'
        function = 'add_new_item'
        datastring= name + desc
        writelog(context, function, 'datastring',datastring)
        return redirect('/')   

    @app.route('/movedoing', methods = ["POST"])
    def movedoing():
        if not github.authorized:
            return redirect(url_for("github.login"))
        id=request.values.get("_id")
#        name=request.values.get("name")
#        desc=request.values.get("desc")
        collection.find({"_id":ObjectId(id)})
        collection.update_one({"_id":ObjectId(id)}, {"$set": {"Status":"In Progress"}})
        context = 'app.py update'
        function = 'movedoing'
        datastring= id
        writelog(context, function, 'datastring',datastring)
        return redirect('/')
    

    @app.route('/movedone', methods = ["POST"])
    def movedone():
        if not github.authorized:
            return redirect(url_for("github.login"))
        id=request.values.get("_id")
        collection.find({"_id":ObjectId(id)})
        collection.update_one({"_id":ObjectId(id)}, {"$set": {"Status":"Completed"}})
        context = 'app.py update'
        function = 'movedone'
        datastring= id
        writelog(context, function, 'datastring',datastring)
        return redirect('/')

    @app.route('/delete', methods = ["POST"])
    def remove():
        if not github.authorized:
            return redirect(url_for("github.login"))
        id=request.values.get("_id")
        collection.find({"_id":ObjectId(id)})
        collection.delete_one({"_id":ObjectId(id)})
        context = 'app.py delete'
        function = 'remove'
        datastring= id
        writelog(context, function, 'datastring',datastring)
        return redirect('/')

    return app

if __name__ == '__main__':
    app = create_app()