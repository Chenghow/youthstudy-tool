import requests,json,main,time,os,re
from urllib import parse
from push import pushplus,email,serverChan

with open('result.json','r',encoding='utf8') as origin_file:
    origin=origin_file.read()
origin=json.loads(origin)
config=main.config

def tokenhandler(method,tokenList):
    for Neededtoken in tokenList:
        if config[method][Neededtoken] == '':
            try:
                if method == 'pushplus':# 保持对旧版的兼容
                    config[method][Neededtoken]=os.environ['PUSHTOKEN']
                else:
                    config[method][Neededtoken]=os.environ[f"{method}_{Neededtoken}"]
            except:
                pass

#当前期完成页
LatestStudy=json.loads(requests.get('https://youthstudy.12355.net/saomah5/api/young/chapter/new',headers=main.headers).text)
StudyId=re.search('[a-z0-9]{10}',LatestStudy['data']['entity']['url']).group(0)
StudyName=LatestStudy['data']['entity']['name']
FinishpageUrl='https://finishpage.dgstu.tk/?id='+StudyId+'&name='+parse.quote(StudyName)

# time.sleep(30)#平台统计有延迟
errorcount=0
for member in origin:
    if member['status']== 'error':
        errorcount+=1
        continue
    try:
        XLtoken=member['XLtoken']
        try:
            profile=main.GetProfile(XLtoken)
            score_now=profile.score()
        except:
            profile=main.GetProfile(main.ConverMidToXLToken(member['member']))
            score_now=profile.score()
        score_add=score_now-member['score']
        if score_now < 100:
            score_need=100-score_now
        elif score_now < 200:
            score_need=200-score_now
        elif score_now < 500:
            score_need=500-score_now
        elif score_now < 1000:
            score_need=1000-score_now
        elif score_now < 5000:
            score_need=5000-score_now
        else:
            score_need=0
        # member['result']+='<br>此次执行增加了<b>'+str(score_add)+'</b>积分'+'<br>当前为<b>'+profile.medal()+'</b>，距离下一徽章还需<b>'+str(score_need)+'</b>积分<br>'
        member['result']['sam']={
            'added':str(score_add),
            'medal':profile.medal(),
            'needed':str(score_need)
        }
        time.sleep(0.2)
    except Exception as e:
        print('出现错误了：'+e)
        member['result']['sam']={
            'added':'Null',
            'medal':'Null',
            'needed':'Null'
        }


if errorcount!=len(main.memberlist):
    titledone=False
    for i in origin:
        if (i['status']!='error') and (i['status']!='passed') and (i['result']['打卡状态']!='本期已过学习时间，下一期请及时学习'):
            if titledone==False:
                title='['+str(len(main.memberlist)-errorcount)+'/'+str(len(main.memberlist))+']'+i['status']+'啦'
                titledone=True#若有打卡成功的则锁定标题
                StudySuccess=True
        else:
            if titledone==False:
                title='['+str(len(main.memberlist)-errorcount)+'/'+str(len(main.memberlist))+']'+'积分任务执行完毕'
                StudySuccess=False
else:
    title='任务执行失败'
    content='所有mid或X-Litemall-Token皆打卡失败'

# HTML推送内容
#隐私信息防剧透隐藏css
htmlcontent='<style>.spoiler{color:#000;background-color:#000}.spoiler:hover{color:#000;background-color:#fff}</style>'
htmlcontent+=f'<a href="{FinishpageUrl}">（伪）当前期完成页</a><br>'
for mem in origin:
    if mem['status']=='error':
        htmlcontent+=f'''<b>mid或X-Litemall-Token:</b><span class="spoiler" >{mem['member']}</span><br><b>出现错误啦</b><br><br>'''
    else:
        htmlcontent+=f'''
        <b>mid或X-Litemall-Token:</b><span class="spoiler" >{mem['member']}</span>
        <b>名称:</b>{mem['name']}
        <b>更新日期:</b>{mem['result']['更新日期']}
        <b>名称:</b>{mem['result']['名称']}
        <b>打卡状态:</b>{mem['result']['打卡状态']}
    '''
        if '往期课程打卡' in mem['result'].keys():
            htmlcontent+=f"<b>往期课程打卡:</b>{mem['result']['往期课程打卡']}<br>"
        htmlcontent+='<b>=====学习频道=====</b><br>'
        if mem['result']['学习频道'] != '跳过执行':
            for channel in mem['result']['学习频道'].keys():
                htmlcontent+=f"<b>{channel}:</b>{mem['result']['学习频道'][channel]}<br>"
        else:
            htmlcontent+='跳过执行<br>'
        htmlcontent+=f"<b>我要答题:</b>{mem['result']['我要答题']}"
        htmlcontent+=f'''
        此次执行增加了<b>{mem['result']['sam']['added']}</b>积分
        当前为<b>{mem['result']['sam']['medal']}</b>，距离下一徽章还需<b>{mem['result']['sam']['needed']}</b>积分<br>
        '''

# 纯文本推送内容
textcontent=f'（伪）当前期完成页：{FinishpageUrl}\n\n'
for mem in origin:
    if mem['status']=='error':
        textcontent+=f'''mid或X-Litemall-Token:{mem['member']}\n出现错误啦\n\n'''
    else:
        textcontent+=f'''mid或X-Litemall-Token:{mem['member']}
        名称:{mem['name']}
        更新日期:{mem['result']['更新日期']}
        名称:{mem['result']['名称']}
        打卡状态:{mem['result']['打卡状态']}
    '''
        if '往期课程打卡' in mem['result'].keys():
            textcontent+=f"往期课程打卡:{mem['result']['往期课程打卡']}\n"
        textcontent+='=====学习频道=====\n'
        if mem['result']['学习频道'] != '跳过执行':
            for channel in mem['result']['学习频道'].keys():
                textcontent+=f"{channel}:{mem['result']['学习频道'][channel]}\n"
        else:
            textcontent+='跳过执行\n'
        textcontent+=f"我要答题:{mem['result']['我要答题']}"
        textcontent+=f'''
        此次执行增加了{mem['result']['sam']['added']}积分
        当前为{mem['result']['sam']['medal']}，距离下一徽章还需{mem['result']['sam']['needed']}积分\n
        '''


# 推送
if config['push']['push']=='yes':
    if (config['push']['time']=='Success' and StudySuccess==True) or config['push']['time']=='all':
        if config['push']['method']=='pushplus':
            tokenhandler('pushplus',['token'])
            pushplus.push(title,htmlcontent,config['pushplus'])
        elif config['push']['method']=='email':
            tokenhandler('email',['host','port','sender','password'])
            email.push(title,htmlcontent,config['email'])
        elif config['push']['method']=='telegram':
            tokenhandler('telegram',['botToken','userId'])
            serverChan.push(title,textcontent,config['telegram'])
        elif config['push']['method']=='severChan':
            tokenhandler('severChan',['key'])
            serverChan.push(title,textcontent,config['severChan'])
    else:
        print('跳过推送')

#Actions Summary
try:
    print('正在生成运行结果')
    summary='## 执行结果\n#### PS：由于安全性问题，详细结果请使用推送功能\n'+f'<a href="{FinishpageUrl}">（伪）当前期完成页</a><br>'+'\n|序号|青年大学习打卡状态|\n|-|-|'
    count=0
    for i in origin:
        count+=1
        summary+='\n|'+str(count)+'|'
        if (i['status'] != 'error') and i['result']['打卡状态']!='本期已过学习时间，下一期请及时学习':
            summary+='✅|'
        else:
            summary+='❌|'
    with open(os.environ['GITHUB_STEP_SUMMARY'],'w+',encoding='utf8') as finaloutput:
        finaloutput.write(summary)
except:
    pass