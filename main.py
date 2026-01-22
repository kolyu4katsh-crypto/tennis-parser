import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_live_scores():
    # URL для получения данных (используем публичное API или парсинг)
    # В данном примере мы настраиваем структуру под ваш HTML
    try:
        # Для начала мы пропишем стабильную выдачу данных
        # Чтобы вы увидели, как меняются цифры на сайте
        matches = [
            {
                "p1": "Никита Мареев", 
                "score": "0:0", 
                "p2": "Алексей Шершнев", 
                "set": "Лига Про - Начало"
            },
            {
                "p1": "Сергей Лопатин", 
                "score": "0:0", 
                "p2": "Иван Солдатов", 
                "set": "Лига Про - Ожидание"
            }
        ]
        return matches
    except Exception as e:
        return [{"p1": "Ошибка", "score": "---", "p2": "связи", "set": str(e)}]

@app.route('/api/live')
def get_live():
    data = get_live_scores()
    return jsonify(data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
  
