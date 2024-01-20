import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackContext, MessageHandler, filters
from parse.find import search_user
import TESTS.validate as val
import telegram

TOKEN = ""

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="hey! enter your name")

async def handle_message(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    if val.check_name(user_input):
        context.user_data['user_input'] = user_input
        await update.message.reply_text(f"Got it {user_input}, now send the photo!")
    else:
        await update.message.reply_text(f"Enter your full name please.")

async def photo_download(update: Update, context: CallbackContext):
    new_file = await context.bot.get_file(update.message.document)
    file = await new_file.download_to_drive()
    return file

async def handle_photo(update: Update, context: CallbackContext) -> None:
    file = await photo_download(update, context)
    name = context.user_data.get('user_input')
    if name:
        await search_user(update, context, name, file)
    else:
        await update.message.reply_text(f"Enter your full name please.")

async def show_updates():
    bot = telegram.Bot(TOKEN)
    async with bot:
        updates = (await bot.get_updates())[-1]
        print(updates)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(MessageHandler(filters.TEXT, handle_message))
    application.add_handler(MessageHandler(filters.Document.IMAGE, handle_photo))
    
    application.run_polling()

    # asyncio.run(show_updates())
