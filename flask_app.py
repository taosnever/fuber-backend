from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "working from flask_app.py"


if __name__ == '__main__':
   # db.create_all()
    app.run()
