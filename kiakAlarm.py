import urllib.request
from bs4 import BeautifulSoup
import datetime
import threading
import os
from twilio.rest import Client

account_sid = 'ACc1ed9fe9d6dd810e1ea76a63c8575b46'
auth_token = '4449045cc63b32f6507f0644ed4ef735'
client = Client(account_sid, auth_token)



period = 10
removeFindedPeriod=6

finded = []


def removeFindedData():
    global finded
    today = datetime.datetime.now().strftime('%Y.%m.%d')

    d1 = today.split('.')
    d1 = datetime.date(int(d1[0]),int(d1[1]),int(d1[2]))
    dellist = []

    for i,x in enumerate(finded):
        d2 = x.split('/')[0].split('.')
        d2 = datetime.date(int(d2[0]),int(d2[1]),int(d2[2]))
        if (d1-d2).days > removeFindedPeriod:
            dellist.append(x)

    for x in dellist:
        finded.remove(x)



def startAlarm():
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
        if data.find('img') != None and len(list(filter(lambda x : title in x,finded)))==0\
                and (d1-d2).days<2:
            str = '{}/{}'.format(time,title)
            res.append(str)
            finded.append(str)

    if len(res)>0:
        client.messages \
            .create(
            body="새 보안권고문",
            from_='+19107086825',
            to='+821053429022'
        )



    print(res)
    print(finded)
    removeFindedData()
    timer.start()





startAlarm()
