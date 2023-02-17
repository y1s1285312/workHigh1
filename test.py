

search_url_prefix = "https://www.google.com/search?q="

#Puppeteer 캡챠우회
from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.chrome.options import Options
import subprocess

subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동


option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

def get_first_result(search_str):
    search_url = search_url_prefix + search_str
    #print(search_url)

    driver = webdriver.Chrome(options=option)
    driver.implicitly_wait(10)

    driver.get(search_url)

    html = driver.page_source
    soup = BeautifulSoup(html,features="html.parser")
    r = str(soup.select('#result-stats'))
    res = r[r.find('약')+1:r.find('개')]
    print(res)
    return res




def makeQry():
    f = open("urls.txt", 'r')
    lines = f.readlines()
    urls=[]

    for line in lines:
        line = line.strip()  # 줄 끝의 줄 바꿈 문자를 제거한다.
        urls.append(line)

    #print(urls)

    f.close()

    f = open("searchs.txt", 'r',encoding='UTF-8')
    lines = f.readlines()
    searchs = []

    for line in lines:
        line = line.strip()  # 줄 끝의 줄 바꿈 문자를 제거한다.
        searchs.append(line)

    #print(searchs)

    f.close()

    qrys=[]

    for url in urls:
        for search in searchs:
            qrys.append(search.replace('[URL]',url))

    #print(qrys)
    return qrys
if __name__ == '__main__':
    qrys=makeQry()
    print(qrys)
    finds=[]

    qry='site:slm.high1.com/ "이력서"'


    result = int(get_first_result(qry))

    print(qry,result)

    if result > 0 :
        finds.append(qry)

    print(qry)





