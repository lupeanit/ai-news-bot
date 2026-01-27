import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime # 날짜를 가져오기 위해 이미 임포트되어 있을 거예요
import pyshorteners

def get_google_news_rss(keyword):
    rss_url = f"https://news.google.com/rss/search?q={keyword}&hl=ko&gl=KR&ceid=KR:ko"
    s = pyshorteners.Shortener()
    
    try:
        response = requests.get(rss_url)
        soup = BeautifulSoup(response.content, features="xml")
        
        items = soup.find_all('item')
        news_data = []
        
        print("🔗 주소 단축 및 데이터 수집 중...")
        
        for i, item in enumerate(items[:10], 1):
            title = item.title.text
            long_url = item.link.text
            try:
                short_url = s.tinyurl.short(long_url)
            except:
                short_url = long_url
            
            pub_date = item.pubDate.text
            news_data.append([i, pub_date, title, short_url])

        # --- [파일명에 날짜 넣기 핵심 부분] ---
        # 오늘 날짜를 '2026-01-27' 같은 형식으로 가져옵니다.
        today_date = datetime.now().strftime('%Y-%m-%d')
        filename = f"AI_뉴스_{today_date}.csv" 
        # -----------------------------------

        with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['번호', '발행시간', '뉴스제목', '단축링크'])
            writer.writerows(news_data)

        print(f"✅ 완료! '{filename}' 파일이 생성되었습니다.")

    except Exception as e:
        print(f"❌ 에러 발생: {e}")

if __name__ == "__main__":
    get_google_news_rss("인공지능")
