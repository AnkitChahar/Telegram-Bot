import requests
import json
import time
import urllib
from bs4 import BeautifulSoup

Token = "402925061:AAEXGpO2dXOxrKsZTiVJPNXA1uoJzxC1-WY"
Url="https://api.telegram.org/bot{}/".format(Token)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset=None):
    url = Url + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = Url + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def echo_all(updates):
    for update in updates["result"]:
        try:
            # text = update["message"]["text"]


            url='https://torrentproject.se/?t='+update["message"]["text"]
            t=requests.get(url).text
            soup=BeautifulSoup(t,'html.parser')
            out=soup.find(class_='tt')
            link=out.find_all('a')
            url2='https://torrentproject.se'+link[3]['href']
            q=requests.get(url2).text
            soup2=BeautifulSoup(q,'html.parser')
            out2=soup2.find(class_='usite')
            link2=out2.find_all('a')
            text=link2[0]['href']


            chat = update["message"]["chat"]["id"]
            send_message(text, chat)
        except Exception as e:
            send_message('Either no torrents were found or There was some unexpected error!', chat)

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()