import requests
from bs4 import BeautifulSoup
import os

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
URL = "https://bestsurefixedmatches.com/"
DB_FILE = "last_content.txt"

def send_message(text):
    if not TOKEN or not CHAT_ID: return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.get(url, params={"chat_id": CHAT_ID, "text": text}, timeout=10)
    except:
        pass

def check_site():
    # 최대한 브라우저처럼 보이게 헤더 보강
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }
    
    try:
        # 1. 사이트 데이터 가져오기
        print(f"{URL} 접속 시도 중...")
        response = requests.get(URL, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        # 사이트의 전체 텍스트 중 앞부분 500자 추출
        current_content = soup.get_text().strip()[:500] 

        # 2. 이전 데이터 확인
        last_content = ""
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r", encoding='utf-8') as f:
                last_content = f.read().strip()

        # 3. 비교 및 알림
        if current_content != last_content:
            send_message(f"✅ 사이트 연결 및 감시 성공!\n새로운 내용이 감지되었습니다.")
            with open(DB_FILE, "w", encoding='utf-8') as f:
                f.write(current_content)
            print("업데이트 발견 및 파일 저장 완료")
        else:
            print("변경 사항 없음")
            
    except Exception as e:
        print(f"접속 실패: {e}")
        # 파일이 없을 때 발생하는 에러 방지를 위해 빈 파일이라도 생성
        if not os.path.exists(DB_FILE):
            with open(DB_FILE, "w", encoding='utf-8') as f:
                f.write("initial")
        # 접속 실패 원인을 텔레그램으로 전송
        send_message(f"⚠️ 접속 오류 발생: 해당 사이트에서 접속을 차단했을 수 있습니다.\n{str(e)[:100]}")

if __name__ == "__main__":
    check_site()
