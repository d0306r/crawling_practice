import pandas as pd
import requests
from bs4 import BeautifulSoup 
import re
from datetime import datetime
import os

query = input("검색어를 입력하세요 : ")
news_num = int(input("크롤링할 기사 개수를 입력하세요 : "))
press_name = input("원하는 언론사 명을 입력하세요 : ")

news_dict = {}
tmp = {}
idx = 0
page = 1
news_url = f'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={query}'

print('기사 수집 중입니다.')
while idx < news_num :   
    
    response = requests.get(news_url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    news_list = soup.select('div.news_area')
    next_page = soup.select('div.sc_page_inner > a.btn')

    for news in news_list :
        title = news.select_one('a.news_tit').text
        link = news.select_one('a.news_tit')['href']
        text = news.select_one('a.api_txt_lines.dsc_txt_wrap').text
        press = news.select_one('a.info.press').text

        if press_name in press :
            news_dict[idx] = {'제목' : title, '링크' : link, '본문 요약' : text, '언론사' : press}
            idx += 1
        else :
            tmp[idx] = {'제목' : title, '링크' : link, '본문 요약' : text, '언론사' : press}
        

    page += 1
    
    for p in next_page :
        if p.text == str(page) :
            news_url = f'https://search.naver.com/search.naver' + p['href']

print('크롤링이 완료되었습니다.')

df = pd.DataFrame(news_dict).T
df.to_excel('news_title_by_press/news_title_by_press.xlsx')
print("저장이 완료되었습니다.")