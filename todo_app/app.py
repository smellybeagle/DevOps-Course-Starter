from todo_app.data.session_items import add_item,get_items
from flask import Flask, redirect,render_template ,request
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())

@app.route('/')
def index():
    items = get_items()
    return render_template('index.html',items_list=items)

@app.route("/add-todo" , methods = ["POST"])
def add_todo():
    item_title= request.form.get("title")
    add_item(item_title)
    return redirect('/')
        
if __name__ == '__main__':
   app.run(debug = True)
