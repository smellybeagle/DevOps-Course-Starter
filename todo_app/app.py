from flask import Flask
from flask import render_template
#from flask import redirect,render_template ,request
from todo_app.flask_config import Config
from todo_app.data.session_items import get_items
app = Flask(__name__)
app.config.from_object(Config())



@app.route('/')
def index():
    items = get_items()
    return render_template('index.html',items=items)

""" @app.route("/add-todo" , methods = ["POST"])
def add_todo():
    item_title= request.form.get("title")
    add_item(item_title)
    return redirect('/') """
        
if __name__ == '__main__':
   app.run(debug = True)
