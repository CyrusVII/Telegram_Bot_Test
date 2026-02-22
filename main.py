from typing import Final
import os

from telegram import Update
from telegram.ext import (
    CommandHandler,
    Application,
    MessageHandler,
    filters,
    ContextTypes
)

# 🔐 TOKEN letto da variabile d'ambiente (Render)
TOKEN: Final[str] = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN non trovato nelle variabili d'ambiente!")

BOT_USERNAME: Final[str] = '@test88_test88_bot'


# =========================
# COMANDI DEL BOT
# =========================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Ciao grazie per il messaggio sono un bot di test'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Ciao varie info'
    )

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Comando custom'
    )


# =========================
# LOGICA RISPOSTE TESTO
# =========================

def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'ciao' in processed:
        return 'Ciao'
    if 'come stai' in processed:
        return 'Sto bene'
    if 'test' in processed:
        return 'Test riuscito'

    return 'Non so cosa hai scritto'


# =========================
# GESTIONE MESSAGGI
# =========================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)

    await update.message.reply_text(response)


# =========================
# ERRORI
# =========================

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f'Update {update} caused error {context.error}')


# =========================
# AVVIO
# =========================

if __name__ == '__main__':

    print('Starting bot...')

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.add_error_handler(error)

    print('Bot is running...')

    app.run_polling()
