import os
import asyncio
from flask import Flask, jsonify, request
from flask_cors import CORS
from telethon import TelegramClient
import openai

app = Flask(__name__)
CORS(app)

API_ID = 28112279 

# Инициализируем клиент без запуска
def get_client(api_hash):
    return TelegramClient('session_mk', API_ID, api_hash)

@app.route('/api/live')
async def live():
    api_hash = request.args.get('hash')
    if not api_hash: 
        return jsonify([{"text": "Ошибка: Настройте API Hash"}]), 400
    
    try:
        client = get_client(api_hash)
        await client.connect()
        # Если не авторизован, отправляем статус на фронтенд
        if not await client.is_user_authorized():
             return jsonify([{"text": "Нужна авторизация в логах Render"}]), 200
             
        messages = await client.get_messages('free_mk', limit=1)
        await client.disconnect()
        return jsonify([{"text": messages[0].message if messages else "Нет матчей"}])
    except Exception as e:
        return jsonify([{"text": f"Ошибка связи: {str(e)}"}]), 500

@app.route('/api/analyze', methods=['POST'])
async def analyze():
    data = request.json
    api_hash = data.get('hash')
    gpt_key = data.get('gpt_key')
    current_game = data.get('game')
    
    if not gpt_key or not api_hash:
        return jsonify({"analysis": "Ошибка: Проверьте ключи в настройках"}), 400

    openai.api_key = gpt_key
    
    try:
        client = get_client(api_hash)
        await client.connect()
        messages = await client.get_messages('free_mk', limit=20)
        history = [m.message for m in messages]
        await client.disconnect()
        
        prompt = f"Экспертный анализ MKX. Текущий бой: {current_game}. История: {history}. Дай прогноз > 2.0. Обоснуй."
        
        # Используем современный метод API
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify({"analysis": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"analysis": f"Ошибка AI: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
  
