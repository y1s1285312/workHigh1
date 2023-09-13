import urllib.request
from bs4 import BeautifulSoup
import datetime
import threading
import requests
import atexit
import smtplib
from email.mime.text import MIMEText

period = 300
removeFindedPeriod = 0

finded = []


def removeFindedData():
    global finded
    today = datetime.datetime.now().strftime('%Y.%m.%d')

    d1 = today.split('.')
    d1 = datetime.date(int(d1[0]), int(d1[1]), int(d1[2]))
    dellist = []

    for i, x in enumerate(finded):
        d2 = x.split('/')[0].split('-')
        d2 = datetime.date(int(d2[0]), int(d2[1]), int(d2[2]))
        if (d1 - d2).days > removeFindedPeriod:
            dellist.append(x)

    for x in dellist:
        print('delData', x)
        finded.remove(x)


def makeMailMsg(title,time,link):
    msg='''
    <header style="margin: 0px; padding: 0px; 
    color: rgb(34, 34, 34); box-sizing: border-box; text-size-adjust: none; -webkit-tap-highlight-color: rgba(0, 0, 0, 0); 
    -webkit-font-smoothing: antialiased; position: relative; border-top: 2px solid rgb(85, 85, 85); font-family: 
    &quot;Noto Sans KR&quot;, Roboto, &quot;Apple SD Gothic Neo&quot;, sans-serif; font-size: 16px; letter-spacing: -0.8px;">
    <div class="b_title" style="margin: 0px; padding: 0px 20px; color: inherit; box-sizing: border-box; text-size-adjust: none;
     -webkit-tap-highlight-color: rgba(0, 0, 0, 0); -webkit-font-smoothing: antialiased; display: inline-block; min-height: 45px; 
     border-style: solid; border-color: rgba(0, 0, 0, 0.15); border-image: initial; border-width: 0px 0px 1px; 
     background: rgb(237, 240, 245); width: 1183.2px;"><h2 style="margin: 0px; padding: 20px 0px; color: 
     inherit; box-sizing: border-box; text-size-adjust: none; -webkit-tap-highlight-color: rgba(0, 0, 0, 0); 
     -webkit-font-smoothing: antialiased; position: relative; clear: both; font-size: 17.6px; min-height: 50px;
      float: left; word-break: break-all;">{}</h2><span style="margin: 0px; padding: 20px 0px; 
      color: inherit; box-sizing: border-box; text-size-adjust: none; -webkit-tap-highlight-color: rgba(0, 0, 0, 0); 
      -webkit-font-smoothing: antialiased; display: inline-block; min-height: 50px; float: right;">{}</span></div></header>
      '''.format(title,time)
    url = 'https://www.krcert.or.kr'+link
    html = urllib.request.urlopen(url).read()
    res = BeautifulSoup(html, 'html.parser')
    datas = str(res.select('#View > div.board > div > div.content_html > table')[0])

    return msg+datas

def sendmail(mailmsg):
    smtp = smtplib.SMTP('smtp.gmail.com', 587)

    smtp.ehlo()

    smtp.starttls()

    smtp.login('y1s1285312@gmail.com', 'aojnpoycjplroaqw')

    msg = MIMEText(mailmsg)
    msg['Subject'] = '보안권고문'

    smtp.sendmail('y1s1285312@gmail.com', 'socmm05@high1.com', msg.as_string())

    smtp.quit()

def startAlarm():
    print('startAlarm')
    msg = ''
    mailmsg=''
    global finded
    today = datetime.datetime.now().strftime('%Y.%m.%d')
    d1 = today.split('.')
    d1 = datetime.date(int(d1[0]), int(d1[1]), int(d1[2]))

    timer = threading.Timer(period, startAlarm)

    url = 'https://www.krcert.or.kr/kr/bbs/list.do?menuNo=205020&bbsId=B0000133'
    html = urllib.request.urlopen(url).read()
    res = BeautifulSoup(html, 'html.parser')
    datas = res.select('#List > div.board > div > table > tbody > tr')
    res = []
    #print(datas)
    for data in datas:
        time = data.find('td', attrs={'class': 'date'}).text
        #print(time)
        title = data.find('td', attrs={'class': 'sbj tal'}).text.strip('\n').strip()
        #print(title)
        link = data.find('td', attrs={'class': 'sbj tal'}).find('a')['href']
        #print(link)
        d2 = time.split('-')
        d2 = datetime.date(int(d2[0]), int(d2[1]), int(d2[2]))
        chk = len(list(filter(lambda x: title in x, finded)))

        if (d1 - d2).days == 0 and chk == 0:
            str = '{}/{}'.format(time, title)
            res.append(str)
            msg += title + '\n'
            mailmsg += makeMailMsg(title,time,link)

            finded.append(str)

    #print('res',res)

    
    if len(res) > 0:
        print('send msg')
        print('res',res)
        print('finded',finded)
        sendmail(mailmsg)
        
        requests.get(
            "https://api.telegram.org/bot5842805214:AAEogW_ZtELsS4zVMvOBfI_jPfvHWIobtNc/sendMessage?chat_id=-1001258042021&text={}".format(
                msg))
    

    removeFindedData()
    timer.start()

def test():
    timer2 = threading.Timer(60, test)

    url = "https://www.high1.com"

    try:
        response = requests.get(url)
        print(response.status_code)

        if response.status_code != 200:
            msg='scode{}'.format(response.status_code)
            #print('200 x')
            requests.get(
            "https://api.telegram.org/bot5842805214:AAEogW_ZtELsS4zVMvOBfI_jPfvHWIobtNc/sendMessage?chat_id=5894259370&text={}".format(
                msg))

    except :
        
        requests.get(
            "https://api.telegram.org/bot5842805214:AAEogW_ZtELsS4zVMvOBfI_jPfvHWIobtNc/sendMessage?chat_id=5894259370&text={}".format(
                'request error'))


    timer2.start()
    
def handle_exit():
    print('종료')


atexit.register(handle_exit)
startAlarm()
test()
