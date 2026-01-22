import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

def fetch_live_scores():
    matches = []
    try:
        # Основной сайт Лиги Про для парсинга
        url = "https://www.ligapro.ru/table-tennis/" 
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Ищем все блоки текущих игр на странице
            items = soup.select('.match-item') # Стандартный класс для Лиги Про
            
            for item in items:
                try:
                    p1 = item.select_one('.player1').text.strip()
                    p2 = item.select_one('.player2').text.strip()
                    score = item.select_one('.score').text.strip()
                    period = item.select_one('.period').text.strip()
                    
                    matches.append({
                        "p1": p1,
                        "p2": p2,
                        "score": score,
                        "set": f"Лига Про - {period}"
                    })
                except:
                    continue

        # Если на сайте сейчас нет матчей (перерыв), создаем уведомление
        if not matches:
            matches = [{"p1": "Ожидание", "p2": "новых игр", "score": "0:0", "set": "Лига Про LIVE"}]
            
    except Exception as e:
        matches = [{"p1": "Ошибка", "p2": "авто-сбора", "score": "---", "set": "Проверка связи"}]
        
    return matches

@app.route('/api/live')
def get_live():
    return jsonify(fetch_live_scores())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
