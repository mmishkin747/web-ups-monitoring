import requests
from environs import Env

env = Env()
env.read_env()


def send_telegram(text: str):
  
    token = env.str("BOT_TOKEN")
    url = "https://api.telegram.org/bot"
    channel_id = env.str("CHANNEL_ID")
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

