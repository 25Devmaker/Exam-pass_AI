import os
import telebot
from dotenv import load_dotenv
from retriever import retrieve
from generator import generate_answer

load_dotenv()

bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))

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

if __name__ == "__main__":
    print("🤖 ExamPass AI Telegram bot is running...")
    bot.polling(none_stop=True)