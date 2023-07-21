from flask import Flask
from .flask_config import Config
from .data.session_items import add_item
from todo_app.data.session_items import add_item
from todo_app.trello_items import get_todo, new_card
from flask import Flask, render_template, request, redirect
from todo_app.flask_config import Config

#import os, requests
app = Flask(__name__)

app.config.from_object(Config())

@app.route('/')
def index():
    #retrieve_items = get_items()
    retrieve_items = get_todo()
    return render_template('index.html', items_list = retrieve_items)


@app.route('/additem', methods = ["POST"])
def add_new_item():
    #new_todo = request.form.get('new-todo')
    new_card()
    return redirect('/')
#x = 'https://api.trello.com/1/cards/64b6455a4fbda32c1ce593c9?key=1a14974b67e88e68f859a2f5236feb25&token=ATTA43e926f02a2de06813db070512611484789561e3f6dfd4eba1539e5b5f32d3ea8B26C75B'
