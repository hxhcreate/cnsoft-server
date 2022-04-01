from flask import Flask
from flask import Flask, url_for, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
import settings

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app, use_native_unicode='utf-8')


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
