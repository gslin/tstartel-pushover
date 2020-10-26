#!/usr/bin/env python3

import configparser
import os
import requests
import selenium
import selenium.webdriver.chrome.options
import sentry_sdk
import time

class Job(object):
    def init_sentry(self):
        home = os.environ['HOME']
        f_conf = '{}/.config/tstartel-pushover/config.ini'.format(home)

        c = configparser.ConfigParser()
        c.read(f_conf)

        sentry_url = c['default']['sentry_url']
        sentry_sdk.init(sentry_url, traces_sample_rate=1.0)

    def main(self):
        self.init_sentry()

        home = os.environ['HOME']
        f_conf = '{}/.config/tstartel-pushover/config.ini'.format(home)

        c = configparser.ConfigParser()
        c.read(f_conf)

        password = c['default']['password']
        pushover_api_token = c['default']['pushover_api_token']
        pushover_user_token = c['default']['pushover_user_token']
        sentry_url = c['default']['sentry_url']
        username = c['default']['username']

        sentry_sdk.init(sentry_url, traces_sample_rate=1.0)

        chrome_options = selenium.webdriver.chrome.options.Options()
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--headless')
        chrome_options.binary_location = '/usr/bin/chromium-browser'

        with selenium.webdriver.Chrome(options=chrome_options) as b:
            url = 'https://www.tstartel.com/CWS/Dashboard_index.php'
            b.get(url)

            i = b.find_element_by_css_selector('#ml_mbrid')
            i.send_keys(username)

            btn = b.find_element_by_css_selector('.btn_primary.next')
            btn.click()

            p = b.find_element_by_css_selector('#ml_mbrpw')
            p.send_keys('')
            p.send_keys(password)

            btn = b.find_element_by_css_selector('#secret .btn_primary.next')
            btn.click()

            # Workaround to wait page rendering.
            time.sleep(30)

            text = b.execute_script('return document.querySelector(".use-status").innerText;')
            text = '{} 的用量：\n'.format(username) + text

            requests.post('https://api.pushover.net/1/messages.json', data={
                'token': pushover_api_token,
                'user': pushover_user_token,
                'message': text,
            })

if '__main__' == __name__:
    j = Job()
    j.main()
