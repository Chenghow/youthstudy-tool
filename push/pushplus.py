import requests,json
def push(title,htmlcontent,config):
    pushplsdata={}
    pushplsdata['channel']=config['channel']
    pushplsdata['template']='html'
    pushplsdata['title']=title
    pushplsdata['content']=htmlcontent
    token=config['token']
    pushplsdata['token']=token
    push=json.loads(requests.post('http://www.pushplus.plus/send/',data=pushplsdata).text)
    if push['msg'] == '请求成功':
        print('推送成功')
    else:
        exit('推送失败：'+push['msg'])