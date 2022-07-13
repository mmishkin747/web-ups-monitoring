

"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""



import requests


def post_telegram(text):
    data={'chat_id':-741325756, 'text':text, 'parse_mode':'Markdown'}
    requests.post('https://api.telegram.org/bot5378416270:AAHzMvey_dlEeGriPQjTD46NJA_5fgE3s1g/sendMessage', data=data)

