
import requests
import json
import clipboard
import os
from vtapi3 import VirusTotalAPIIPAddresses, VirusTotalAPIError



vt_api_ip_addresses = VirusTotalAPIIPAddresses('0ee2afa4471af7973368d8d056e1dd991f66026eb42fcaf4e41257614785793c')
'''
f = open('iplist.txt', 'r')
iplists = f.readlines()
f.close()
'''

data = clipboard.paste()
iplists = data.split('\r\n')
#print(iplists)
findlist=''
totalcount = 0
for ip in iplists:
    if totalcount >15:
        break
    try:
        result = vt_api_ip_addresses.get_report(ip)

    except VirusTotalAPIError as err:
        print(err, err.err_code)
    else:
        if vt_api_ip_addresses.get_last_http_error() == vt_api_ip_addresses.HTTP_OK:
            result = json.loads(result)
            #result = json.dumps(result, sort_keys=False, indent=4)

        else:
            print('HTTP Error [' + str(vt_api_ip_addresses.get_last_http_error()) + ']')

    datas = result['data']['attributes']['last_analysis_results']
    risk =0
    for k,data in datas.items():
        if data['category'] =='malicious':
            risk+=1

    datas = result['data']['attributes']
    #country = datas['country']
    #as_owner = datas['as_owner']
    last_analysis_stats = sum(datas['last_analysis_stats'].values())
    res = '{}/{}'.format(risk,last_analysis_stats)

    if risk > 4 :
        findlist += '{}\n'.format(ip)
        print(ip, res)
        totalcount+=1
        continue

    headers = {
        'accept': 'application/json',
        'Authorization': 'Basic NTRmYTU1YmQtZjgzNC00ZTkyLWI1ODItYTQ1NDExOGUzOGM0OjE2YWNjZThkLWVhYTUtNDlmMi05NWRhLWRiM2M5ZmFkZWFiMQ==',
    }


    response = requests.get('https://api.xforce.ibmcloud.com/api/ipr/{}'.format(ip), headers=headers)
    ret = response.content.decode()
    datas = json.loads(ret)
    datas = datas['history'][-1]
    score = datas['score']
    print(ip, res, score)

    if score > 4:
        findlist += '{}\n'.format(ip)
        totalcount += 1


print('####findlist####')
print(findlist)
os.system('pause')








