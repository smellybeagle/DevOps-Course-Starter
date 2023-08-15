from typing import ItemsView
from flask import Flask


from .flask_config import Config
from todo_app.trello_items import init_trello, todolists, doinglists, donelists,new_card,move_doing,move_done
from flask import Flask, render_template, request, redirect
from todo_app.view_model import ViewModel


app = Flask(__name__)
app.config.from_object(Config())

init_trello()

@app.route('/')
def index():
    todo_items = todolists()
    doing_items = doinglists()
    done_items = donelists()
    item_view_model = ViewModel(todo_items, doing_items, done_items)
    #return render_template('index.html', view_model=item_view_model)
    return render_template('index.html', view_model = item_view_model)

@app.route('/additem', methods = ["POST"])
def add_new_item():
    new_card()
    return redirect('/')

@app.route('/movedoing', methods = ["POST"])
def movedoing():
    move_doing()
    return redirect('/')

@app.route('/movedone', methods = ["POST"])
def movedone():
    move_done()
    return redirect('/')
