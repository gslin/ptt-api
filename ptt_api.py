#!/usr/bin/env python3

import asyncio
import bottle
import configparser
import json
import logging
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

async def get_user_ip(id):
    origin = 'https://term.ptt.cc'
    uri = 'wss://ws.ptt.cc/bbs'

    config = configparser.ConfigParser()
    config.read('{}/.config/ptt-api/account.ini'.format(os.environ['HOME']))

    login_password = config['default']['password']
    login_username = config['default']['username']

    home_re = re.compile('《上次故鄉》(\d+\.\d+\.\d+\.\d+)')

    logging.info('Connecting...')
    async with websockets.connect(uri, timeout=3, origin=origin) as ws:
        buf = ''
        while True:
            r = await ws.recv()
            buf += r.decode('big5', 'ignore')

            if '請輸入代號' in buf:
                logging.info('Sending username...')
                await ws.send((login_username + "\r").encode('utf-8'))

                buf = ''
                continue

            if '請輸入您的密碼' in buf:
                logging.info('Sending password...')
                await ws.send((login_password + "\r").encode('utf-8'))

                buf = ''
                continue

            if '您想刪除其他重複登入的連線嗎' in buf:
                await ws.send("n\r".encode('utf-8'))

                buf = ''
                continue

            if '您要刪除以上錯誤嘗試的記錄嗎' in buf:
                await ws.send("n\r".encode('utf-8'))

                buf = ''
                continue

            if '請勿頻繁登入以免造成系統過度負荷' in buf:
                await ws.send("\r".encode('utf-8'))

                buf = ''
                continue

            if '休閒聊天區' in buf:
                await ws.send("t\rq\r".encode('utf-8'))

                buf = ''
                continue

            if '請輸入使用者代號' in buf:
                logging.info('Query...')
                await ws.send((id + "\r").encode('utf-8'))

                buf = ''
                continue

            if '上次故鄉' in buf:
                t = home_re.search(buf)
                if t is not None:
                    return t[1]

                break

            if '請按任意鍵繼續' in buf:
                logging.info('Pressing enter...')
                await ws.send("\r".encode('utf-8'))

                buf = ''
                continue

    return None

@app.route('/user/<id>')
def user(id):
    loop = asyncio.get_event_loop()
    ip = loop.run_until_complete(asyncio.gather(get_user_ip(id)))
    loop.close()

    bottle.response.set_header('Cache-Control', 'max-age=60,public')
    bottle.response.set_header('Content-Type', 'application/json')

    return json.dumps({'id': id, 'ip': ip})

if __name__ == '__main__':
    if os.environ.get('PORT'):
        port = int(os.environ.get('PORT'))
    else:
        port = 8080

    bottle.run(app=app, host='0.0.0.0', port=port)
