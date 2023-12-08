from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

url = 'https://velog.io/'
driver = webdriver.Chrome() 
driver.get(url)
time.sleep(5)
start_time = time.time()
END_TIME = 100

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
    page_source = driver.page_source 
    soup = BeautifulSoup(page_source, 'lxml')

post_html = soup.select('body > div > div.BasicLayout_block__6bmSl > div.responsive_mainResponsive___uG64 > div > div.BasicLayout_mainWrapper__xXO4A > main > div.PostCardGrid_block__ZeuvW > div')

cnt = 0
posts = []
for element in post_html:
    cnt = cnt + 1
    title = element.select_one('h4.PostCard_h4__Yj8PZ').get_text(strip=True)
    comments = element.select_one('div.PostCard_subInfo__aMAtH > span:nth-child(3)').get_text(strip=True)
    good_cnt = element.select_one('div.PostCard_likes__pWcUv').get_text(strip=True)
    sub_title = element.select_one('div.PostCard_descriptionWrapper__x6u1q').get_text(strip=True)
    posts.append({'title': title, 'comment': comments, 'good_cnt': good_cnt, 'sub_title': sub_title})
    
posts = posts[:200]
retrospect = [post for post in posts if '회고' in post['title']] # 회고 관련 글
keywords = ['에러', '해결', '이슈', '트러블 슈팅']
issue = [post for post in posts if any(keyword in post['title'] for keyword in keywords)] # 에러 해결 글

#인기글 전체 좋아요, 댓글 수 평균
all_avg_comments = sum(int(re.findall(r'\d+', post['comment'])[0]) for post in posts) / len(posts)
all_avg_good_cnt = sum(int(re.findall(r'\d+', post['good_cnt'])[0]) for post in posts) / len(posts)

#issue의 평균 댓글 수, retrospect의 평균 좋아요 수
issue_avg_comments = sum(int(re.findall(r'\d+', post['comment'])[0]) for post in issue) / len(issue)
retrospect_avg_good_cnt = sum(int(re.findall(r'\d+', post['good_cnt'])[0]) for post in retrospect) / len(retrospect)

print("인기글 중 에러 해결글 갯수: ", len(issue)) 
print("인기글 중 회고글 갯수: ", len(retrospect))
print("게시물 총 갯수: ", len(posts))

print ("인기글의 평균 댓글 수: ", all_avg_comments)
print ("인기글의 평균 좋아요 수: ", all_avg_good_cnt)

print("인기글 중 에러 해결글의 평균 댓글 수: ", issue_avg_comments)
print("인기글 중 회고글의 평균 좋아요 수: ", retrospect_avg_good_cnt)

# 'title'과 'sub_title'에서의 모든 단어를 추출
words = ''
for post in posts:
    words += post['title'] + ' ' + post['sub_title']

# 불용어 리스트 생성
stopwords = set(['이', '이제', '위해', '때문에', '하고', '만큼','한','을', '은', '는', '이','가', '대해', '어떤', '그'])

# 불용어를 제거한 텍스트 생성
filtered_words = ' '.join(word for word in words.split() if word not in stopwords)

# 워드 클라우드 생성, 이때 'font_path' 옵션에 폰트의 경로를 지정해줍니다.
wordcloud = WordCloud(font_path='/Users/ahnyunji/Library/Fonts/Puradak Gentle Gothic OTF.otf',
                      width=800, height=800, background_color='white').generate(filtered_words)

# 워드 클라우드 시각화
plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)

plt.show()