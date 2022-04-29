import requests,json
import time

# 获取时间戳
t = int(round(time.time()* 1000))

cookies = {
    'UM_distinctid': '17ff782a7d232c-0e128337366389-796b0158-56d10-17ff782a7d4c1',
    'Hm_lvt_149ef6fe5d623c086adc1622cf6c0df1': '1649125010',
    'Hm_lpvt_149ef6fe5d623c086adc1622cf6c0df1': '1649125014',
}

#如不使用github actions，请删除下方注释并手动设定xLitemallToken
#xLitemallToken=""

headers = {
    'Host': 'youthstudy.12355.net',
    'Connection': 'keep-alive',
    'X-Litemall-Token': xLitemallToken,
    'X-Litemall-IdentiFication': 'young',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; Redmi K30 5G Build/SKQ1.220119.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3189 MMWEBSDK/20220105 Mobile Safari/537.36 MMWEBID/1350 MicroMessenger/8.0.19.2080(0x28001337) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64',
    'Accept': '*/*',
    'Origin': 'https://youthstudy.12355.net',
    'X-Requested-With': 'com.tencent.mm',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://youthstudy.12355.net/h5/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
}

headersj = {
    'Host': 'youthstudy.12355.net',
    'Connection': 'keep-alive',
    'X-Litemall-Token': xLitemallToken,
    'X-Litemall-IdentiFication': 'young',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; Redmi K30 5G Build/SKQ1.220119.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3189 MMWEBSDK/20220105 Mobile Safari/537.36 MMWEBID/1350 MicroMessenger/8.0.19.2080(0x28001337) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64',
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'X-Requested-With': 'com.tencent.mm',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://youthstudy.12355.net/h5/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
}
# 签到
print("开始签到:")
mark = requests.get('https://youthstudy.12355.net/saomah5/api/young/mark/add', headers=headersj)
msg=json.loads(mark.text).get('msg')
print(msg)
# 获得最新学习章节
latest = requests.get('https://youthstudy.12355.net/saomah5/api/young/chapter/new', headers=headersj, cookies=cookies)


chapterId=json.loads(latest.text).get('data').get('entity').get('id')
updateDate=json.loads(latest.text).get('data').get('entity').get('updateDate')
name=json.loads(latest.text).get('data').get('entity').get('name')

data = {
    'chapterId': chapterId,
}
# 打卡
print("打卡最新一期青年大学习:")
saveHistory = requests.post('https://youthstudy.12355.net/saomah5/api/young/course/chapter/saveHistory', headers=headers, cookies=cookies, data=data)
#print(saveHistory.text)

print("更新日期:",updateDate,"名称:",name,"打卡状态:",json.loads(saveHistory.text).get('msg'))


#获得题目
print("刷题:")
getList = requests.get('https://youthstudy.12355.net/saomah5/api/question/list', headers=headersj)
#print(getList.text)
questionlist=json.loads(getList.text).get("data").get("list")
submit_output=''
for questions in questionlist:
    #print(questions['id'])
    json_data = {
    'dataId': questions['id'],
    'commitDetails': [
        {
            'questionId': '1510063654195441665',
            'answer': '2,3,4',
            'active': True,
            'questionType': 1,
        },
        {
            'questionId': '1510063654187053058',
            'answer': '2,4',
            'active': True,
            'questionType': 1,
        },
        {
            'questionId': '1510063654203830274',
            'answer': '1,2,4',
            'active': True,
            'questionType': 1,
        },
        {
            'questionId': '1510063654208024578',
            'answer': '1,2,4',
            'active': True,
            'questionType': 1,
        },
        {
            'questionId': '1510063654191247361',
            'answer': '1,3',
            'active': True,
            'questionType': 1,
        },
    ],
    }
    #刷题
    submit = requests.post('https://youthstudy.12355.net/saomah5/api/question/submit/question', headers=headers, json=json_data)
    print(json.loads(submit.text).get('msg'),end="")
    submit_output=submit_output+json.loads(submit.text).get('msg')
'''
#获取季
getcourse = requests.get('https://youthstudy.12355.net/saomah5/api/young/course/list', headers=headersj)
courselist=json.loads(getcourse.text).get("data").get("list")
for course in courselist:
    #获取期
    #print(course['id'])
    params = {
        'id': course['id'],
    }
    getdetail = requests.get('https://youthstudy.12355.net/saomah5/api/young/course/detail', headers=headersj, params=params)
'''
output={}
output['title']=name+'签到'+json.loads(saveHistory.text).get('msg')
output['result']="更新日期:"+updateDate+"\n名称:"+name+"\n打卡状态:"+json.loads(saveHistory.text).get('msg')+"\n刷题：\n"+submit_output
with open('result.txt','a',encoding='utf8') as new_file:
    new_file.write(str(output))
