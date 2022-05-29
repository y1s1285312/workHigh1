import requests
import json
import clipboard
import os

'''
url = "https://exchange.xforce.ibmcloud.com/ip/8.8.8.8"
html = requests.get(url)
soup = BeautifulSoup(html.text, 'html.parser')
risk = soup.select('#searchresults > div > div.instantresultwrapper > div.risklevelbar.low > div.scorebackgroundfilter.numtitle')
print(soup)
'''

headers = {
    'accept': 'application/json',
    #'accept': 'text/html',
    'Authorization': 'Basic NTRmYTU1YmQtZjgzNC00ZTkyLWI1ODItYTQ1NDExOGUzOGM0OjE2YWNjZThkLWVhYTUtNDlmMi05NWRhLWRiM2M5ZmFkZWFiMQ==',
}

url = 'https://api.xforce.ibmcloud.com/api/ipr/{}'

data = clipboard.paste()
iplists = data.split('\r\n')
#print(iplists)
findlist=''

for ip in iplists:
    if '.' not in ip :
        continue
    print(ip,end=' ')
    response = requests.get(url.format(ip), headers=headers)
    res = response.content.decode()
    datas = json.loads(res)
    datas = datas['history'][-1]
    score = datas['score']
    print(score)

    if score > 4 :
        findlist += '{}\n'.format(ip)

print('####findlist####')
print(findlist)
os.system('pause')

