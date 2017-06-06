#!/usr/bin/env python
# coding:utf-8

import uuid
import time
from functools import wraps

from flask import Flask, render_template, redirect, request
from flask_socketio import SocketIO, emit
from flask_login import LoginManager, current_user, login_user

app = Flask(__name__)
app.config['SECRET_KEY'] = str(uuid.uuid4())
login_manager = LoginManager(app)
socketio = SocketIO(app)
user_manager = None


class User(object):

    def __init__(self, username, password):
        self.uid = int(time.time() * 100)
        self.username = username
        # TODO: 密码存储
        self.password = password
        self.join_time = time.time()
        self.last_active_time = time.time()

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.uid


class UserManager(object):
    """用户管理类

    Attributes:
        UserDB: 用户数据库
    """

    def __init__(self, UserDB=dict()):
        # nametuple('user', 'uid username password join_time last_active_time')
        self.db = UserDB

    def create(self, user: User):
        if user.uid not in self.db:
            self.db[user.uid] = user
        else:
            return self.db.get(user.uid)

    def load(self, user_id):
        return self.db.get(user_id, None)

@login_manager.user_loader
def load_user(user_id):
    return user_manager.load(user_id)

def login_required(redirect_to='/login'):
    def decorate(f):
        @wraps(decorate)
        def fc(*args, **kw):
            if current_user.is_authenticated:
                return f(*args, **kw)
            else:
                return redirect(redirect_to)
        return fc
    return decorate

@app.route('/', methods=['GET', 'POST'])
@login_required()
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User(username, password)
        user_manager.create(user)
        login_user(user)
        return "login as {username} {password}".format(username=username, password=password)
    else:
        raise NotImplementedError

@socketio.on('message')
def chat(msg):
    print('recv msg: {}'.format(msg))
    socketio.emit('response', msg.get('msg'))

def load_data():
    global user_manager
    user_manager = UserManager()


if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0')
