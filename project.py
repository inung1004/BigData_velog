from selenium import webdriver
from bs4 import BeautifulSoup
import time

url = 'https://velog.io/'
driver = webdriver.Chrome() 
driver.get(url)
time.sleep(5)
start_time = time.time()
END_TIME = 90

while True:
    last_height = driver.execute_script("return document.body.scrollHeight") 
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
        time.sleep(2)  
        new_height = driver.execute_script("return document.body.scrollHeight")  
        if new_height == last_height: 
            break
        last_height = new_height

       
        if time.time() - start_time > END_TIME:
            break

    if time.time() - start_time > END_TIME:
        break
    page_source = driver.page_source  # 페이지의 HTML 소스를 가져옵니다.
    soup = BeautifulSoup(page_source, 'lxml')

data = soup.select('body > div > div.BasicLayout_block__6bmSl > div.responsive_mainResponsive___uG64 > div > div.BasicLayout_mainWrapper__xXO4A > main > div > div > div > a > h4')
# print(data)
cnt = 0
for text in data:
  cnt = cnt + 1
  print(text.get_text())
print(cnt)