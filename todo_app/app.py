from flask import Flask, render_template
from todo_app.flask_config import Config
from todo_app.data.session_items import get_items
app = Flask(__name__)

@app.route('/')
def index():
    def get_items():
        def add_item(title):
            return render_template('index.html',get_items=all,add_item=title)

if __name__ == '__main__':
   app.run(debug = True)
