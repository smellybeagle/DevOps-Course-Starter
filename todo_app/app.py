# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config())
    
#     from flask import Flask
#     from todo_app.viewmodel import ViewModel
#     from .flask_config import Config
#     from todo_app.trello_items import todolists, doinglists, donelists,new_card,move_doing,move_done
#     from flask import Flask, render_template, request, redirect
    
#     @app.route('/')
#     def index():
#         todo_items = todolists()
#         doing_items = doinglists()
#         done_items = donelists()
#         item_view_model = ViewModel(todo_items,doing_items,done_items)
#         return render_template('index.html', view_model=item_view_model)
#     #return render_template('index.html', todo_list = todo_items, doing_list = doing_items, done_list = done_items)
    
#     @app.route('/additem', methods = ["POST"])
#     def add_new_item():
#         new_card()
#         return redirect('/')

#     @app.route('/movedoing', methods = ["POST"])
#     def movedoing():
#         move_doing()
#         return redirect('/')

#     @app.route('/movedone', methods = ["POST"])
#     def movedone():
#         move_done()
#         return redirect('/')   
  
#     return app

from flask import Flask


from .flask_config import Config
from todo_app.trello_items import todolists, doinglists, donelists,new_card,move_doing,move_done
from flask import Flask, render_template, request, redirect


app = Flask(__name__)
app.config.from_object(Config())

#init_trello()

@app.route('/')
def index():
    todo_items = todolists()
    doing_items = doinglists()
    done_items = donelists()
    return render_template('index.html', todo_list = todo_items, doing_list = doing_items, done_list = done_items)

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
