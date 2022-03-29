# -*- coding = utf-8 -*-
# @Time : 2022/3/29 21:02
# @Author : AuYang
# @File : app.py
# @Software : PyCharm

from flask import Flask, request, render_template, make_response, session, redirect, url_for

app = Flask(__name__)
app.secret_key = b'auyang'

@app.route("/", methods=['GET', 'POST'])
def index():
    if 'username' in session:
        res = make_response(render_template('welcome.html', method=request.method, data=request.data.decode()))
        res.set_cookie('username', 'the username')
        return res
    else:
        app.logger.error("user not login")
        return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        app.logger.debug("user login")
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    else:
        return render_template('login.html')