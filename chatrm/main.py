#!/usr/bin/env python
# coding:utf-8

import uuid
import time
from functools import wraps

from flask import Flask, render_template, redirect, request, flash
from flask_socketio import SocketIO, emit
from flask_login import LoginManager, current_user, login_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = str(uuid.uuid4())
login_manager = LoginManager(app)
socketio = SocketIO(app)
user_manager = None


class User(object):

    def __init__(self, username, password, nickname=''):
        self.uid = user_manager.generate_uid
        self.username = username
        self.nickname = nickname or username
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
        return self.username


class UserManager(object):
    """用户管理类

    Attributes:
        UserDB: 用户数据库
    """

    def __init__(self, UserDB=dict()):
        # nametuple('user', 'uid nickname password join_time last_active_time')
        self.db = UserDB
        self.db['user_nums'] = 0

    def create(self, username, password):
        if username not in self.db:
            self.db[username] = User(username, password)
            self.db['user_nums'] += 1
            return self.db.get(username)
        else:
            raise Exception("user exist")

    def load(self, username):
        return self.db.get(username, None)

    @property
    def generate_uid(self):
        return self.db.get('user_nums') + 1

@login_manager.user_loader
def load_user(user_id):
    return user_manager.load(user_id)

def login_required(redirect_to='/login'):
    def decorate(f):
        @wraps(f)
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 前端验证填入字段

        # try:
        #     user = user_manager.create(username, password)
        # except:
        #     flash("用户名已被注册")
        #     return redirect('/register')
        user = user_manager.create(username, password)
        login_user(user)
        return redirect('/')
    else:
        raise NotImplementedError


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = user_manager.load(username)
        if not user:
            flash("用户不存在")
            return redirect('/login')
        if password != user.password:
            flash("密码不正确")
            return redirect('/login')
        login_user(user)
        return redirect('/')
    else:
        raise NotImplementedError


@app.route('/logout')
@login_required()
def logout():
    logout_user()
    return redirect('/login')

@socketio.on('message')
def chat(msg):
    print('recv msg: {}'.format(msg))
    socketio.emit('response', msg.get('msg'))

def load_data():
    global user_manager
    user_manager = UserManager()


if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0')
