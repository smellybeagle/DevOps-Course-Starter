from typing import ItemsView
from flask import Flask, render_template,request,redirect,url_for # For flask implementation
#from pymongo import MongoClient # Database connector
from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId # For ObjectId to work
from bson.errors import InvalidId # For catching InvalidId exception for ObjectId
import os
from todo_app.flask_config import Config
from todo_app.view_model import ViewModel

                          

mongodb_host = os.environ.get('MONGO_HOST', 'localhost')
mongodb_port = int(os.environ.get('MONGO_PORT', '27017'))
client = MongoClient(mongodb_host, mongodb_port)    #Configure the connection to the database
db = client.todo_app    #Select the database
todos = db.todolist #Select the collection

#from todo_app.data.item import Item


def todolists():
	#Display the Uncompleted Tasks
	todos_l = todos.find({"done":"no"})
	a2="active"
	return todos_l

#def doinglists():
#	doing = todos.find({"done":"no"})
#	a2="active"
#    return doing

#def donelists():
#	todos_l = todos.find({"done":"yes"})
#	a3="active"
 #   return todos_l