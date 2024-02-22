import requests,json,time,re,os,configparser
import urllib.parse

apiHeaders = {
  'Host': 'tuanapi.12355.net',
  'Connection': 'keep-alive',
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'Origin': 'https://tuan.12355.net',
  'User-Agent': 'MicroMessenger',
  'X-Requested-With': 'com.tencent.mm',
  'Sec-Fetch-Site': 'same-site',
  'Sec-Fetch-Mode': 'cors',
  'Referer': 'https://tuan.12355.net/wechat/view/YouthLearning/page.html',
  'Accept-Encoding': 'gzip, deflate',
  'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
}
youthstudyHeaders = {
        'Host': 'youthstudy.12355.net',
        'Connection': 'keep-alive',
        'Content-Length': '134',
        'Origin': 'https://youthstudy.12355.net',
        'X-Litemall-Token': '',
        'X-Litemall-IdentiFication': 'young',
        'User-Agent': 'MicroMessenger',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'X-Requested-With': 'com.tencent.mm',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Referer': 'https://youthstudy.12355.net/h5/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }
headers = {
    'Host': 'youthstudy.12355.net',
    'Connection': 'keep-alive',
    'X-Litemall-Token': '',
    'X-Litemall-IdentiFication': 'young',
    'User-Agent': 'MicroMessenger',
    'Accept': '*/*',
    'Origin': 'https://youthstudy.12355.net',
    'X-Requested-With': 'com.tencent.mm',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://youthstudy.12355.net/h5/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
}
#读取配置
config = configparser.ConfigParser()
#默认配置
config['study'] = {
    'youthstudy': 'yes',
    'dailycheckin': 'yes',
    'studychannel': 'yes',
    'answer_questions': 'yes'
}
config['push'] = {
    'push': 'yes',
    'channel': 'wechat'
}
if os.path.exists('config.ini'):#若存在配置文件则依照配置文件执行
    config.read('config.ini')
else:
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

#获取成员列表
try:
    member=os.environ['MEMBER']
except:
    try:
        with open('member.txt','r',encoding='utf8') as member_file:
            member=member_file.read()
    except:
        open('member.txt','x',encoding='utf8')
        print('已创建member.txt，请添加mid或者XLToken后重新运行！（一行一个或以"|"分隔）')
        exit()
#检查member
if member != '':
    pass
else:
    exit('+================+\n| member未定义！ |\n+================+')

#清除所有空字符并以|或换行符分割字符串创建列表
if re.search('\|',member):
    memberlist=(("".join(member.split()))).split('|')
else:
    memberlist=(member.replace(' ','').rstrip('\n').split('\n'))

#获取积分、徽章
class GetProfile:
    def __init__(self,input):
        headers['X-Litemall-Token']=input
        self.profile_dist=json.loads(requests.get('https://youthstudy.12355.net/saomah5/api/myself/get',headers=headers).text)
    def score(self):
        return(self.profile_dist['data']['entity']['score'])
    def medal(self):
        try:
            return(self.profile_dist['data']['entity']['medal']['name'])
        except:
            return('无徽章信息')
    def name(self):
        return(self.profile_dist['data']['entity']['nickName'])
    def StudyRecords(self):
        return(json.loads(requests.get('https://youthstudy.12355.net/saomah5/api/young/course/record/page?pageNo=1&pageSize=300',headers=headers).text)['data']['list'])

#转换mid
def ConverMidToXLToken(raw):
    if re.match('[a-zA-Z]',raw):
        return(raw)
    else:
        try:
            payload='sign='+urllib.parse.quote((json.loads(requests.get('https://tuanapi.12355.net/questionnaire/getYouthLearningUrl?mid='+str(raw),headers=apiHeaders).text))['youthLearningUrl'].replace('https://youthstudy.12355.net/h5/#/?sign=',''))
            rp=json.loads((requests.post('https://youthstudy.12355.net/apih5/api/user/get',headers=youthstudyHeaders,data=payload)).text)
            return(rp['data']['entity']['token'])
        except Exception as e:
            raise Exception('mid转换失败')

# 时间戳
def t():
    return(int(round(time.time()* 1000)))

#是否达每日积分到限制
def islimited(XLToken):
    headers['X-Litemall-Token']=XLToken
    try:
        return(json.loads(requests.get('https://youthstudy.12355.net/saomah5/api/young/score/status',headers=headers).text)['data']['entity']['scoreStatus'])
    except Exception as e:
        raise Exception('获取积分限制失败:')
output_list=[]
if __name__ == '__main__':
    count=0
    statusOutput=''#存储执行状态的字符串
    for member in memberlist:
        count+=1
        print('\t\t\t\t===============当前用户序号:',count,'===============\t\t\t\t')
        try:
            #将mid转换为xLitemallToken
            xLitemallToken=ConverMidToXLToken(member)
            profile=GetProfile(xLitemallToken)#初始化类

            score=profile.score()#获取打卡前积分，用于后续计算
            # 每日签到
            print('=====每日签到=====')
            if config['study']['dailycheckin']=='yes':
                mark = requests.get('https://youthstudy.12355.net/saomah5/api/young/mark/add', headers=headers)
                msg=json.loads(mark.text).get('msg')
                print(msg)
            else:
                print('跳过执行')

            # 青年大学习打卡
            # 获得最新学习章节
            latest = requests.get('https://youthstudy.12355.net/saomah5/api/young/chapter/new', headers=headers)

            chapterId=json.loads(latest.text).get('data').get('entity').get('id')
            updateDate=json.loads(latest.text).get('data').get('entity').get('updateDate')
            name=json.loads(latest.text).get('data').get('entity').get('name')

            data = {
                'chapterId': chapterId,
            }
            # 打卡
            print('\n=====打卡最新一期青年大学习======')
            for records in profile.StudyRecords():
                if records['dataName']==name:
                    IsStudied=True
                    break
                else:
                    IsStudied=False
            if config['study']['youthstudy']=='yes':
                if IsStudied==True:
                    StudyStatus='当期已学习，自动跳过'
                else:
                    saveHistory = requests.post('https://youthstudy.12355.net/saomah5/api/young/course/chapter/saveHistory', headers=headers, data=data)
                    StudyStatus=json.loads(saveHistory.text).get('msg')
            else:
                StudyStatus='跳过执行'
            print('更新日期:',updateDate,'\n名称:',name,'\n打卡状态:',StudyStatus)


            #学习频道
            channelList = json.loads(requests.get('https://youthstudy.12355.net/saomah5/api/channel/tier/one/list', headers=headers).text).get('data').get('list')#主动获取学习频道栏目
            print('\n=====学习频道=====')
            channel_output={}
            if config['study']['studychannel'] == 'yes':
                for i in channelList:
                    id = i['id']
                    channelName = i['channelName']
                    print(channelName,end='：')
                    # channelNow='<b>'+channelName+':</b>'
                    
                    params = {
                        'channelId': id,
                        'pageSize': '999',#提高pageSize以获得全部元素
                        'time': t(),
                    }
                    if islimited(xLitemallToken) == False:
                        getarticle = requests.get('https://youthstudy.12355.net/saomah5/api/article/get/channel/article', params=params, headers=headers)
                        articleslist = json.loads(getarticle.text).get('data').get('entity').get('articlesList')
                        addScore_output=''
                        availableArticles=0
                        for articles in articleslist:
                            if articles['scoreStatus'] == False:
                                params = {
                                    'id': articles['id'],
                                }
                                addScore = requests.get('https://youthstudy.12355.net/saomah5/api/article/addScore', params=params, headers=headers)
                                print(json.loads(addScore.text).get('msg'),end='')
                                addScore_output+=json.loads(addScore.text).get('msg')
                                availableArticles+=1
                        if availableArticles==0:
                            print('无可供学习内容')
                            addScore_output+='无可供学习内容'
                        else:
                            print('')
                    else:
                        print('达到每日积分限制，跳过执行')
                        addScore_output='达到每日积分限制，跳过执行'
                    # channel_output+=channelNow+addScore_output
                    channel_output[channelName]=addScore_output

                # channel_output=channel_output.rstrip('<br>')
            else:
                channel_output='跳过执行'
                print(channel_output)
            #我要答题
            print('我要答题：',end='')
            if config['study']['answer_questions']=='yes':
                if islimited(xLitemallToken) == False:
                    #获得题目
                    testList=json.loads(requests.get('https://youthstudy.12355.net/saomah5/api/question/list', headers=headers).text).get('data').get('list')#获取题目列表
                    submit_output=''
                    for test in testList:
                        params = {
                            'dataId': test['id'],
                            'time': t(),
                        }
                        #获取小题答案等信息
                        testDetail = requests.get('https://youthstudy.12355.net/saomah5/api/question/detail', params=params,headers=headers)
                        questionList=json.loads(testDetail.text).get('data').get('list')
                        commitDetails=[]
                        for i in range(len(questionList)):
                            answerNum=[ord(s)-64 for s in list(questionList[i]['trueAnswer'])]#将列表内的字母换为数字
                            answerStr = [str(x) for x in answerNum]#将列表内的数字换为字符串
                            answer=','.join(answerStr)#将列表换为字符串
                            emptyDict={'questionId': questionList[i]['id'],'answer': answer,'active': True,'questionType': questionList[i]['type']}
                            commitDetails.append(emptyDict)
                        json_data={
                            'dataId':test['id'],
                            'commitDetails':commitDetails
                        }
                        #刷题
                        submit = requests.post('https://youthstudy.12355.net/saomah5/api/question/submit/question', headers=headers, json=json_data)
                        print(json.loads(submit.text).get('msg'),end='')
                        submit_output=submit_output+json.loads(submit.text).get('msg')
                    print('\n')
                else:
                    print('达到每日积分限制，跳过执行')
                    submit_output='达到每日积分限制，跳过执行'
            else:
                submit_output='跳过执行'
                print(submit_output)

            statusOutput=statusOutput+str(count)+'\t'+StudyStatus+'\n'
            output={}
            output['member']=member
            output['XLtoken']=xLitemallToken
            output['name']=profile.name()
            if IsStudied==True or config['study']['youthstudy']!='yes':
                output['status']='passed'
            else:
                output['status']=name+'签到'+json.loads(saveHistory.text).get('msg')
            # output['result']='<b>更新日期:</b>'+updateDate+'<br><b>名称:</b>'+name+'<br><b>打卡状态:</b>'+StudyStatus+'<br><b>=====学习频道=====</b><br>'+channel_output+'<br><b>我要答题:</b>'+submit_output
            output['result']={'更新日期':updateDate,
                              '名称':name,
                              '打卡状态':StudyStatus,
                              '学习频道':channel_output,
                              '我要答题':submit_output}
            output['score']=score
            output_list.append(output)
        except Exception as e:
            print('出现错误啦:'+str(e)+'\n')
            statusOutput=statusOutput+str(count)+'\terror\n'
            output_list.append({'member':member,'status':'error'})
    print('\n执行结果如下:')
    print('序号\t'+'青年大学习打卡状态')
    print(statusOutput)
    if 'error' in statusOutput:
        print('出现错误啦！可能的原因有:\n1.您的网络\n2.您的mid或X-Litemall-Token有误\n3.其他问题(如知晓请反馈)')
    with open('result.json','w+',encoding='utf8') as new_file:
        new_file.write(json.dumps(output_list))