import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

# Функция для сбора реальных данных
def fetch_liga_pro_live():
    matches = []
    try:
        # Используем один из стабильных агрегаторов Лиги Про
        url = "https://www.ligapro.ru/table-tennis/" 
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Поиск блоков с матчами (логика под структуру сайта Лиги Про)
            items = soup.find_all('div', class_='match-item') # Пример класса
            
            for item in items:
                try:
                    p1 = item.find('div', class_='player1').text.strip()
                    p2 = item.find('div', class_='player2').text.strip()
                    score = item.find('div', class_='current-score').text.strip()
                    status = item.find('div', class_='match-status').text.strip()
                    
                    matches.append({
                        "p1": p1,
                        "p2": p2,
                        "score": score,
                        "set": status
                    })
                except:
                    continue
        
        # Если сайт пуст (ночные перерывы), отдаем заглушку, чтобы видеть работу
        if not matches:
            matches = [{"p1": "Ожидание", "p2": "Матчей", "score": "0:0", "set": "Лига Про LIVE"}]
            
    except Exception as e:
        print(f"Ошибка парсинга: {e}")
        matches = [{"p1": "Ошибка", "p2": "Связи", "score": "---", "set": "Проверьте URL"}]
        
    return matches

@app.route('/api/live')
def get_live():
    data = fetch_liga_pro_live()
    return jsonify(data)

if __name__ == "__main__":
    # Render сам передает нужный порт
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
