import os, requests
from flask import Flask, render_template, redirect, request
import json
from todo_app.data.item import Item
import pymongo
#from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId # For ObjectId to work
from bson.errors import InvalidId # For catching InvalidId exception for ObjectId
from .flask_config import Config
#from todo_app.trello_items import init_trello, todolists, doinglists, donelists,new_card,move_doing,move_done
from todo_app.view_model import ViewModel

mongodb_host = os.getenv("MONGO_HOST")
mongodb_port = os.getenv("MONGO_PORT")
client = pymongo.MongoClient()
client = pymongo.MongoClient(mongodb_host, mongodb_port)    #Configure the connection to the database
db = client.todo_app    #Select the database
todos = db.todolist #Select the collection


def init_mongo():
  # declare which variables from outside the function we'll be changing
  global todo, doing, done


def todolists():
	#Display the Uncompleted Tasks
	todo = todos.find({"status":"To Do"})
	return todo
def doinglists():
	#Display the Uncompleted Tasks
	doing = todos.find({"status":"In Progress"})
	return doing
def donelists():
	#Display the Uncompleted Tasks
	done = todos.find({"status":"Complete"})
	return done


headers = {"Accept": "application/json"}

def new_card():
     name = request.form.get('name','desc','date','status')
     requests.request("POST",url, headers=headers, params=query_params)


def move_doing():
     dbid = request.form.get('id')
     query_params = {"idList": envdoing,"key": trello_key, "token": trello_token}
     requests.request("PUT",url3, headers=headers, params=query_params)


def move_done():
     trelloid = request.form.get('id')
     url3 = 'https://api.trello.com/1/cards/' + trelloid 
     query_params = {"idList": envdone,"key": trello_key, "token": trello_token}
     print(f"URL: {url3}")
     requests.request("PUT",url3, headers=headers, params=query_params)