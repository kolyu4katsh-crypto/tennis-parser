import os
import asyncio
from flask import Flask, jsonify, request
from flask_cors import CORS
from telethon import TelegramClient
import openai

app = Flask(__name__)
CORS(app)

# Настройки подключения к Telegram (API ID оставляем в коде, остальное - через запросы)
API_ID = 28112279 

@app.route('/api/live')
async def live():
    # Мы будем получать данные из настроек, переданных через заголовки или параметры
    api_hash = request.args.get('hash')
    if not api_hash: return jsonify([{"text": "Введите API Hash в настройках"}])
    
    client = TelegramClient('session_mk', API_ID, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        return jsonify([{"text": "Нужна авторизация в Telegram (см. логи Render)"}])
    
    messages = await client.get_messages('free_mk', limit=1)
    return jsonify([{"text": messages[0].message if messages else "Нет матчей"}])

@app.route('/api/analyze', methods=['POST'])
async def analyze():
    data = request.json
    api_hash = data.get('hash')
    gpt_key = data.get('gpt_key')
    current_game = data.get('game')
    
    openai.api_key = gpt_key
    
    # Собираем историю 20 игр
    client = TelegramClient('session_mk', API_ID, api_hash)
    await client.connect()
    messages = await client.get_messages('free_mk', limit=20)
    history = [m.message for m in messages]
    
    prompt = f"Ты эксперт MKX. Проанализируй бой: {current_game}. История: {history}. Дай прогноз с кэфом >2.0 (Победа аутсайдера, Фаталити или Бруталити). Обоснуй."

    response = await openai.ChatCompletion.acreate(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return jsonify({"analysis": response.choices[0].message.content})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
  
