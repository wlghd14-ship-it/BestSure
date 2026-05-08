import requests
from bs4 import BeautifulSoup
import os

# 환경변수 불러오기
TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
URL = "https://bestsurefixedmatches.com/"
DB_FILE = "last_content.txt"

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": text}
    requests.get(url, params=params)

def check_site():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 사이트의 메인 내용을 감지 (사이트 마다 다를 수 있음)
        target = soup.find('main') or soup.find('body')
        current_content = target.text.strip()[:200] # 상위 200자만 비교

        # 이전 데이터 읽기
        last_content = ""
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r", encoding='utf-8') as f:
                last_content = f.read().strip()

        # 새로운 내용이 있으면 알림
        if current_content != last_content:
            send_message(f"🔔 사이트 업데이트 감지!\n\n바로가기: {URL}")
            with open(DB_FILE, "w", encoding='utf-8') as f:
                f.write(current_content)
            print("성공: 업데이트 감지 및 메시지 전송 완료")
        else:
            print("알림: 변경 사항 없음")
            
    except Exception as e:
        print(f"에러 발생: {e}")

if __name__ == "__main__":
    check_site()
