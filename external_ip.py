#!/usr/bin/env python3
import requests

url = "http://api.ipify.org/"

resp = requests.get(url)
if resp.status_code == 200:
    ip = resp.text
    print(resp.text)
