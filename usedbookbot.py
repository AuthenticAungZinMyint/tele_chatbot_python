import logging
from typing import Final
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup )
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters)

TOKEN : Final = "7455922128:AAF0FhMII61CYs2sttdY5hjAe61DtC15fgQ"
BOT_USERNAME : Final = "@chatw1thm3bot"


#Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

#Define State
BOOK_GENRE, BOOK_TITLE, BOOK_PRICE, PHOTO, SUMMARY = range(5)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """"Start conversation and ask for used book's categorie"""
    reply_keyboard = [['Thriller', 'Translation', 'Rare', 'Novel', 'Literature']]
    await update.message.reply_text(
        "<b>Welcome to the used book selling Bot!\n"
        "Let's get some detail about the book you're selling.\n"
        "What is your book's genere?</b>",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return BOOK_GENRE

async def book_genre(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the user's book genre and ask for book title"""
    user = update.message.from_user
    context.user_data['book_genre'] = update.message.text
    logger.info('Book genre of %s: %s', user.first_name, update.message.text)
    await update.message.reply_text(
        f"<b>You selected {update.message.text} book.\n"
        f"What is your book title?</b>",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove()
    )
    return BOOK_TITLE

async def book_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Store book title and ask for price"""
    user = update.message.from_user
    context.user_data['book_title'] = update.message.text
    logger.info('Book title of %s: %s', user.first_name, update.message.text)
    await update.message.reply_text(
        f"<b>Your book title is {update.message.text}\n"
        f"Expected price of your book?</b>",
        parse_mode="HTML"
    )
    return BOOK_PRICE

async def book_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stroe price and ask for photo"""
    user = update.message.from_user
    context.user_data['book_price'] = update.message.text
    logger.info('Book price of %s: %s', user.first_name, update.message.text)
    await update.message.reply_text(
        "<b>Success! updated the price of book\n"
        "Now Please upload a photo of your book</b>",
        parse_mode="HTML"
    )
    return PHOTO

async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store the photo"""
    photo_file = await update.message.photo[-1].get_file()
    #Correctly store the file_id of upload photo for later use
    context.user_data['book_photo'] = photo_file.file_id
    
    #informed user summary
    await update.message.reply_text(
        "<b>Success! photo uploaded\n"
        "Let's summarize your book selling</b>",
        parse_mode="HTML"
    )
    await summary(update, context)

async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Summarize user's book sale"""
    details = context.user_data
    #arrange summary
    summary_text = (
        f"<b>Here's what you told about your book:\n</b>"
        f"<b>Book Genre:</b> {details.get('book_genre')}\n"
        f"<b>Book Title:</b> {details.get('book_title')}\n"
        f"<b>Book Price:</b> {details.get('book_price')}\n"
        f"<b>Book Photo:</b> {"uploaded" if "book_photo" in details else "Not provided"}"
    )
    chat_id = update.effective_chat.id
    
    if 'book_photo' in details and details['book_photo'] != "Not Provided":
        await context.bot.send_photo(chat_id=chat_id, photo=details['book_photo'], caption=summary_text, parse_mode="HTML" )
    else:
        await context.bot.send_message(chat_id=chat_id, text=summary_text, parse_mode="HTML" )
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text("Bye! When you have used book to sell, come here again!\n" "Have a good day!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main() -> None:
    """Run the bot"""
    application = Application.builder().token(TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            BOOK_GENRE: [MessageHandler(filters.TEXT & ~filters.COMMAND, book_genre)],
            BOOK_TITLE: [MessageHandler(filters.TEXT, book_title)],
            BOOK_PRICE: [MessageHandler(filters.TEXT, book_price)],
            PHOTO: [MessageHandler(filters.PHOTO, photo)],
            SUMMARY: [MessageHandler(filters.ALL, summary)]
                
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    application.add_handler(conv_handler)
    
    #handle when user not in conversation but send start
    application.add_handler(CommandHandler('start', start))
    
    print("Polling...")
    application.run_polling(poll_interval=5)
    
if __name__ == "__main__":
    main()    

    