import os
import requests
import telebot
from flask import Flask, request
from dotenv import load_dotenv
from retriever import retrieve
from generator import generate_answer

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SPACE_URL = os.getenv("SPACE_URL")  # e.g. https://devmaker25-devnexusbot.hf.space

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(func=lambda message: True)
def handle_question(message):
    question = message.text.strip()
    thinking_msg = bot.reply_to(message, "🔍 Searching your syllabus...")

    try:
        chunks = retrieve(question)
        result = generate_answer(question, chunks)

        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=thinking_msg.message_id,
            text=result["answer"]
        )

        if result["images"]:
            for img in result["images"]:
                if os.path.exists(img["path"]):
                    with open(img["path"], "rb") as photo:
                        bot.send_photo(
                            message.chat.id,
                            photo,
                            caption=f"📊 Diagram from page {img['page']}"
                        )

    except Exception as e:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=thinking_msg.message_id,
            text="❌ Something went wrong. Please try again."
        )
        print(f"Error: {str(e)}")

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_data = request.get_json()
    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return "ok", 200

@app.route("/")
def index():
    return "ExamPass AI is running!", 200

def set_webhook():
    webhook_url = f"{SPACE_URL}/{TOKEN}"
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)
    print(f"✅ Webhook set to {webhook_url}")

if __name__ == "__main__":
    print("🤖 ExamPass AI Telegram bot is running...")
    bot.polling(none_stop=True)