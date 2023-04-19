# 필요한 패키지 설치
import pandas as pd
import requests
from bs4 import BeautifulSoup 
import re
from datetime import datetime
import os

# 변수 입력
query = input("검색할 키워드를 입력하세요 : ")
query = query.replace(" ", "+")
news_num = int(input("필요한 뉴스 기사의 개수를 입력해주세요 : "))

# 준비
news_url = f"https://search.naver.com/search.naver?where=news&sm=tab_jum&query={query}"
req = requests.get(news_url)

idx = 0
news_dict = {}
page = 1

while idx < news_num :
    if req.status_code == 200 :
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        ul = soup.find('ul', {'class' : 'list_news'})
        titles = ul.select('li > div > div > a')

        for title in titles :
            headline = title.text
            news_dict[idx] = {'title' : headline, 'url' : title.get('href')}
            idx += 1
            
        page += 1 

        next = soup.find('div', {'class' : 'sc_page_inner'}).find_all('a')
        for n in range(len(next)) :
            if next[n].text == str(page) : 
                news_url = 'https://search.naver.com/search.naver' + next[n].get('href')
    
        req = requests.get(news_url)
        
    else :
        print(req.status_code)
        print("페이지 접근 실패")

# 결과 저장
df = pd.DataFrame(news_dict).T
df.to_excel("../crawling/news_title_crawling.xlsx")
print("저장이 완료되었습니다.")