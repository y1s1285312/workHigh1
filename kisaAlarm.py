import urllib.request
from bs4 import BeautifulSoup
import datetime
import threading
import requests
import atexit

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
        d2 = x.split('/')[0].split('.')
        d2 = datetime.date(int(d2[0]), int(d2[1]), int(d2[2]))
        if (d1 - d2).days > removeFindedPeriod:
            dellist.append(x)

    for x in dellist:
        print('delData',x)
        finded.remove(x)


def startAlarm():
    print('startAlarm')
    msg='새 보안권고문\n'
    global finded
    today = datetime.datetime.now().strftime('%Y.%m.%d')
    d1 = today.split('.')
    d1 = datetime.date(int(d1[0]), int(d1[1]), int(d1[2]))

    timer = threading.Timer(period, startAlarm)

    url = 'https://krcert.or.kr/data/secNoticeList.do'
    html = urllib.request.urlopen(url).read()
    res = BeautifulSoup(html, 'html.parser')
    datas = res.select('#contentDiv > table > tbody > tr')
    res = []

    for data in datas:
        time = data.find_all('td', attrs={'class': 'gray'})[2].text
        title = data.find('td', attrs={'class': 'colTit'}).text.strip('\n')
        d2 = time.split('.')
        d2 = datetime.date(int(d2[0]), int(d2[1]), int(d2[2]))
        chk = len(list(filter(lambda x: title in x, finded)))

        if (d1 - d2).days == 0 and chk == 0:
            str = '{}/{}'.format(time, title)
            res.append(str)
            msg += title+'\n'
            finded.append(str)

    if len(res) > 0:
        print('send msg')
        print(res)
        print(finded)
        requests.get("https://api.telegram.org/bot5842805214:AAEogW_ZtELsS4zVMvOBfI_jPfvHWIobtNc/sendMessage?chat_id=5894259370&text={}".format(msg))

    
    removeFindedData()
    timer.start()

def handle_exit():
    print('종료')

atexit.register(handle_exit)
startAlarm()
