import os
import requests
from dotenv import load_dotenv
import telebot
from retriever import retrieve
from generator import generate_answer
load_dotenv()

bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))

@bot.message_handler(func=lambda message: True)
def handle_question(message):
    question = message.text.strip()

    # Step 1: Reply immediately so Telegram doesn't timeout
    thinking_msg = bot.reply_to(message, "🔍 Searching your syllabus...")

    try:
        # Step 2: Now do the slow work
        chunks = retrieve(question)
        result = generate_answer(question, chunks)

        # Step 3: Edit the thinking message with the actual answer
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=thinking_msg.message_id,
            text=result["answer"]
        )

        # Step 4: Send images if found
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
print("🤖 ExamPass AI Telegram bot is running...")
bot.polling(none_stop=True)