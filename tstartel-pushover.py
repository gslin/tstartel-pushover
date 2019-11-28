#!/usr/bin/env python3

import configparser
import mechanicalsoup
import os
import re
import requests

def work():
    home = os.environ['HOME']
    f_conf = '{}/.config/tstartel-pushover/config.ini'.format(home)

    c = configparser.ConfigParser()
    c.read(f_conf)

    password = c['default']['password']
    pushover_api_token = c['default']['pushover_api_token']
    pushover_user_token = c['default']['pushover_user_token']
    username = c['default']['username']

    b = mechanicalsoup.StatefulBrowser()

    url = 'https://sso.tstartel.com/mc-ws/MC/MCLogin.action?sid=mytstar&ru=https://sso.tstartel.com/MyTstar/MyDashboard.action&cid=001,009,025,026'
    b.open(url)

    f = b.select_form('#form1')
    f.set('msisdn', username)
    f.set('password', password)
    b.submit_selected()

    url = 'https://sso.tstartel.com/MyTstar/normal/MyDashboard.action'
    b.open(url)

    text = b.get_current_page().select('.user-static li')[0].text.strip()
    text = re.sub(r'\s+', ' ', text, flags=re.DOTALL)

    text = '{} 的用量：\n'.format(username) + text

    requests.post('https://api.pushover.net/1/messages.json', data={
        'token': pushover_api_token,
        'user': pushover_user_token,
        'message': text,
    })

if '__main__' == __name__:
    work()
