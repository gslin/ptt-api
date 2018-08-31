#!/usr/bin/env python3

import asyncio
import bottle
import configparser
import os
import re
import websockets

app = application = bottle.Bottle()

@app.route('/')
def index():
    bottle.redirect('https://github.com/gslin/ptt-api')

@app.route('/robots.txt')
def robotstxt():
    bottle.response.set_header('Content-Type', 'text/plain')
    return '#\nUser-agent: *\nDisallow: /\n'

@app.route('/user/<username>')
def user(username):
    origin = 'https://term.ptt.cc'
    uri = 'wss://ws.ptt.cc/bbs'

    config = configparser.ConfigParser()
    config.read('{}/.config/ptt-api/account.ini'.format(os.environ['HOME']))

    login_password = config['default']['password']
    login_username = config['default']['username']

    home_re = re.compile('《上次故鄉》(\d+\.\d+\.\d+\.\d+)')

if __name__ == '__main__':
    if os.environ.get('PORT'):
        port = int(os.environ.get('PORT'))
    else:
        port = 8080

    bottle.run(app=app, host='0.0.0.0', port=port)
