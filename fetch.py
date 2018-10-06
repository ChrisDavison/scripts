"""Fetch and print URLs"""
import sys
import requests


for url in sys.argv[1:]:
    response = requests.get(url)
    if response.text:
        print(response.text)
