import requests
import json
import clipboard
import os
headers = {
    'accept': 'application/json',
    'Authorization': 'Basic NTRmYTU1YmQtZjgzNC00ZTkyLWI1ODItYTQ1NDExOGUzOGM0OjE2YWNjZThkLWVhYTUtNDlmMi05NWRhLWRiM2M5ZmFkZWFiMQ==',
}


data = clipboard.paste()
iplists = data.split('\r\n')
#print(iplists)
findlist=''

for ip in iplists:
    response = requests.get('https://api.xforce.ibmcloud.com/api/ipr/{}'.format(ip), headers=headers)
    res = response.content.decode()
    datas = json.loads(res)
    datas = datas['history'][-1]
    score = datas['score']
    print(ip,score)

    if score > 4 :
        findlist += '{}\n'.format(ip)

print('####findlist####')
print(findlist)
os.system('pause')