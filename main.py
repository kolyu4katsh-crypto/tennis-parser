import os
import time
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/live')
def get_live():
    # Тестовые данные для проверки связи с вашим HTML
    data = [
        {"p1": "Александр Кольмин", "s1": 11, "p2": "Олег Барашков", "s2": 1, "set": "Идет 3-я партия"},
        {"p1": "Максим Мамека", "s1": 1, "p2": "Александр Письменный", "s2": 2, "set": "Идет 1-я партия"}
    ]
    return jsonify(data)

if __name__ == "__main__":
    # Railway сам назначит порт через переменную окружения
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
  
