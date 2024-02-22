import requests
def push(title,textcontent,config):
    server='https://api.telegram.org'
    url = server +  '/bot' + config['botToken'] + '/sendMessage'
    ret = requests.post(url, data={'chat_id': config['userId'], 'text': textcontent}, headers={
                  'Content-Type': 'application/x-www-form-urlencoded'})
    print('Telegram response: \n', ret.status_code)
    if ret.status_code != 200:
        print(ret.content.decode('utf-8'))