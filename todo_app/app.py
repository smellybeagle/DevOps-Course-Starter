from flask import Flask
from .flask_config import Config
#from .data.session_items import add_item
#from todo_app.data.session_items import add_item
from todo_app.trello_items import todolists, doinglists, donelists,new_card,move_done
from flask import Flask, render_template, request, redirect
from todo_app.flask_config import Config


#import os, requests
app = Flask(__name__)

app.config.from_object(Config())

@app.route('/')
def index():
    #retrieve_items = get_items()
    #retrieve_items = get_lists()
    todo_items = todolists()
    doing_items = doinglists()
    done_items = donelists()
    return render_template('index.html', todo_list = todo_items, doing_list = doing_items, done_list = done_items)

@app.route('/additem', methods = ["POST"])
def add_new_item():
    #create_card()
    #name = request.form.get('name')
    new_card()
    #request.form.get['new_todo']
    return redirect('/')

@app.route('/movedoing', methods = ["POST"])
def movedoing():
    #create_card()
    move_done()
    return redirect('/')

@app.route('/movetodone', methods = ["POST"])
def movedone():
    #create_card()
    move_done()
    return redirect('/')