from flask import Flask
from flask import render_template,redirect, request, render_template_string
from todo_app.flask_config import Config
from todo_app.data.session_items import get_items,add_item

app = Flask(__name__)
app.config.from_object(Config())



@app.route('/')
def index():
    items = get_items()
    return render_template('index.html',items=items)
    #return render_template_string('''<form action="/add-todo" method="POST"><button type="submit" name="Submit" value="Submit">Submit</button></form>''')

@app.route("/add-todo" , methods = ["POST"])
def add_todo():
    item_title= request.form.get("title")
    add_item(item_title)
    return redirect('/')
        
if __name__ == '__main__':
   app.run(debug = True)
