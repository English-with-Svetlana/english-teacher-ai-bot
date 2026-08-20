import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from groq import Groq

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
You are English Teacher AI, a friendly English teacher.

The user may write in English or Russian.

Your job:
- check English sentences for grammar mistakes;
- correct mistakes;
- explain grammar clearly and simply;
- translate between Russian and English when asked;
- answer questions about English;
- help the user practise English.

Keep explanations short and easy to understand.
If you correct a sentence, show:
❌ Original sentence
✅ Correct sentence
💡 Short explanation

You may explain grammar in Russian if the user writes in Russian.
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! I'm English Teacher AI.\n\n"
        "I can:\n"
        "✏️ check your English grammar\n"
        "💡 explain grammar rules\n"
        "🌍 translate Russian ↔ English\n"
        "💬 answer questions about English\n\n"
        "Send me a sentence or a question!"
    )


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
            ],
        )

        ai_answer = response.choices[0].message.content
        await update.message.reply_text(ai_answer)

    except Exception as e:
        print(e)
        await update.message.reply_text(
            "Sorry, something went wrong. Please try again."
        )


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, answer)
    )

    print("English Teacher AI is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
