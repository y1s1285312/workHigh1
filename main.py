import urllib.request
from bs4 import BeautifulSoup

search_url_prefix = "https://www.google.com/search?q="

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import subprocess
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By




def get_first_result(search_str):
    search_url = search_url_prefix + search_str


    try:
        driver.get(search_url)
        sleep(1)
        f1 = driver.find_elements(By.TAG_NAME, "iframe")[0]
        driver.switch_to.frame(f1)

        sleep(2)

        driver.find_element(By.XPATH, "//span[@id='recaptcha-anchor']").click()
        driver.switch_to.default_content()

        sleep(5)

        f2 = driver.find_elements(By.TAG_NAME, "iframe")[2]

        driver.switch_to.frame(f2)
        print('move frame')

        driver.find_element(By.XPATH, '//*[@id="rc-imageselect"]/div[3]/div[2]/div[1]/div[1]/div[4]').click()


        sleep(5)

        driver.find_element(By.XPATH, '//*[@id="rc-audio"]/div[8]/div[2]/div[1]/div[1]/div[4]').click()

        sleep(3)




    except Exception as e :
        pass
        #print(e)

    #sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, features="html.parser")

    r = str(soup.select('#result-stats'))
    res = r[r.find('약') + 1:r.find('개')]
    #print(res)
    return res



'''
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
    
'''


sp = subprocess.Popen(
            r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')  # 디버거 크롬 구동

option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)


if __name__ == '__main__':
    #qrys=makeQry()
    #print(qrys)

    f = open("urls.txt", 'r')
    lines = f.readlines()
    urls = []

    for line in lines:
        line = line.strip()  # 줄 끝의 줄 바꿈 문자를 제거한다.
        urls.append(line)

    # print(urls)

    f.close()

    f = open("searchs.txt", 'r', encoding='UTF-8')
    lines = f.readlines()
    searchs = []

    for line in lines:
        line = line.strip()  # 줄 끝의 줄 바꿈 문자를 제거한다.
        searchs.append(line)

    # print(searchs)

    f.close()


    finds=[]



    for url in urls :


        for search in searchs:
            qry=search.replace('[URL]',url)
            result = True

            while result == True:
                try:
                    result = get_first_result(qry)
                    result=int(result)
                    print(qry, result)
                except:
                    result = True







            if result > 0 :
                finds.append(qry)

    print('result\n')
    if len(finds)>0:
        print('\n'.join(finds))
    driver.close()
    sp.terminate()





