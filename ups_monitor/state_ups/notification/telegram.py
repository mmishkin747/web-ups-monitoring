import requests


def send_telegram(text: str):
    """
    data={'chat_id':-741325756, 'text':text, 'parse_mode':'Markdown'}
    req = requests.post('https://api.telegram.org/bot5378416270:AAHzMvey_dlEeGriPQjTD46NJA_5fgE3s1g/sendMessage', data=data)
    print(req.status_code)
    """

    token = "5378416270:AAHzMvey_dlEeGriPQjTD46NJA_5fgE3s1g"
    url = "https://api.telegram.org/bot"
    channel_id = "-741325756"
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
         "chat_id": channel_id,
         "text": text
          })
    
    if r.status_code != 200:
        print("post_text error")
        raise Exception("post_text error")
    return r.status_code

