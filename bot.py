import os
import logging
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import MessageHandler, CommandHandler, ApplicationBuilder, filters, ContextTypes

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Доброго времени суток. Как вас зовут?')


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('До свидания!')
    context.application.stop()


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.text
    usd_rate = get_uds_rate()
    if usd_rate:
        message = f'Рад знакомству, {user_name}! Курс доллара сегодня {usd_rate} руб.'
    else:
        message = f'Рад знакомству, {user_name}! К сожалению не удалось получить курс доллара'
    await update.message.reply_text(message)


def get_uds_rate():
    try:
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
        data = response.json()
        rub_rate = data['rates']['RUB']
        return rub_rate
    except Exception as e:
        print(f'Ошибка при получении курса {e}')
        return None


def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('stop', stop))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()


if __name__ == '__main__':
    main()
