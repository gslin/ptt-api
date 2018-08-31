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

async def get_user_ip(username):
    origin = 'https://term.ptt.cc'
    uri = 'wss://ws.ptt.cc/bbs'

    config = configparser.ConfigParser()
    config.read('{}/.config/ptt-api/account.ini'.format(os.environ['HOME']))

    login_password = config['default']['password']
    login_username = config['default']['username']

    home_re = re.compile('《上次故鄉》(\d+\.\d+\.\d+\.\d+)')

    async with websockets.connect(uri, timeout=3, origin=origin) as ws:
        buf = ''
        while True:
            r = await ws.recv()
            buf += r.decode('big5', 'ignore')

            if '請輸入代號' in buf:
                break

        await ws.send((login_username + "\r\n").encode('utf-8'))
        buf = ''
        while True:
            r = await ws.recv()
            buf += r.decode('big5', 'ignore')

            if '請輸入您的密碼' in buf:
                break

        await ws.send((login_password + "\r\n").encode('utf-8'))

        await ws.send("\x1b[OD\x1b[ODt\r\nq\r\n".encode('utf-8'))

        buf = ''
        while True:
            r = await ws.recv()
            buf += r.decode('big5', 'ignore')

            if '請輸入使用者代號' in buf:
                break

        await ws.send((username + "\r\n").encode('utf-8'))

        buf = ''
        while True:
            r = await ws.recv()
            buf += r.decode('big5', 'ignore')

            if '請按任意鍵繼續' in buf:
                break

        t = home_re.search(buf)
        if t is not None:
            return t[1]

    return None

@app.route('/user/<username>')
def user(username):
    loop = asyncio.get_event_loop()
    ip = loop.run_until_complete(asyncio.gather(get_user_ip(username)))
    loop.close()

    return ip

if __name__ == '__main__':
    if os.environ.get('PORT'):
        port = int(os.environ.get('PORT'))
    else:
        port = 8080

    bottle.run(app=app, host='0.0.0.0', port=port)
