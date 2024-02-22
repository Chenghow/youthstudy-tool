import requests
def push(title,textcontent,config):
    url = 'https://sctapi.ftqq.com/' + config['key'] + '.send'
    requests.post(url, data={"text": title, "desp": textcontent})