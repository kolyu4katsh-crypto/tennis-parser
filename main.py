import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_real_liga_pro_data():
    # В этом блоке мы прописываем текущих игроков из вашего приложения
    try:
        # Эти данные появятся на вашем сайте через 1 минуту после сохранения
        live_matches = [
            {"p1": "Никита Мареев", "score": "0:0", "p2": "Алексей Шершнев", "set": "Лига Про LIVE"},
            {"p1": "Сергей Лопатин", "score": "0:0", "p2": "Иван Солдатов", "set": "Лига Про LIVE"},
            {"p1": "Юрий Кривенький", "score": "3:1", "p2": "Соперник", "set": "Идет 2-я партия"}
        ]
        return live_matches
    except:
        return [{"p1": "Ошибка", "score": "---", "p2": "данных", "set": "Render"}]

@app.route('/api/live')
def get_live():
    return jsonify(get_real_liga_pro_data())

if __name__ == "__main__":
    # Render автоматически подставит порт
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
