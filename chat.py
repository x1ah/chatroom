#!/usr/bin/env python
# coding:utf-8

from chatrm.main import socketio, app, load_data


if __name__ == "__main__":
    load_data()
    socketio.run(app, debug=True, host='0.0.0.0')
