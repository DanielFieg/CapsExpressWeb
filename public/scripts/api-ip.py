#!/usr/bin/env python3

import requests

username = "u66cd4bf7547005a8-zone-custom"  # Seu nome de usuário do 2Captcha
password = "u66cd4bf7547005a8"  # Sua senha do 2Captcha
PROXY_DNS = "43.152.113.55:2334"  # Substitua pelo seu proxy
urlToGet = "http://ip-api.com/json"
proxy = {"http":"http://{}:{}@{}".format(username, password, PROXY_DNS)}
r = requests.get(urlToGet , proxies=proxy)

print("Response:{}".format(r.text))
