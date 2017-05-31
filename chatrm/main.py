#!/usr/bin/env python
# coding:utf-8

import uuid

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = str(uuid.uuid4())
socketio = SocketIO(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@socketio.on('send_message')
def chat(msg):
    print('recv msg: {}'.format(msg))
    emit('send_message', msg)


if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0')
