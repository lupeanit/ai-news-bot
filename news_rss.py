import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import pyshorteners # URL 단축 도구 추가

def get_google_news_rss(keyword):
    rss_url = f"https://news.google.com/rss/search?q={keyword}&hl=ko&gl=KR&ceid=KR:ko"
    s = pyshorteners.Shortener() # 단축기 실행
    
    try:
        response = requests.get(rss_url)
        soup = BeautifulSoup(response.content, features="xml")
        
        items = soup.find_all('item')
        news_data = []
        
        print("🔗 주소 단축 중... 잠시만 기다려주세요.")
        
        for i, item in enumerate(items[:10], 1): # 단축 속도를 위해 10개만 추천
            title = item.title.text
            long_url = item.link.text
            
            # TinyURL 서비스를 사용하여 길고 복잡한 주소를 짧게 줄임
            try:
                short_url = s.tinyurl.short(long_url)
            except:
                short_url = long_url # 에러 발생 시 원래 주소 사용
            
            pub_date = item.pubDate.text
            news_data.append([i, pub_date, title, short_url])

        filename = "Cloud_AI_News_Short.csv"
        with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['번호', '발행시간', '뉴스제목', '단축링크'])
            writer.writerows(news_data)

        print(f"✅ 단축 완료! '{filename}' 파일을 확인하세요.")

    except Exception as e:
        print(f"❌ 에러 발생: {e}")

if __name__ == "__main__":
    get_google_news_rss("인공지능")