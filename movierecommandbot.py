import logging
from typing import Final
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters)

TOKEN : Final = "7455922128:AAF0FhMII61CYs2sttdY5hjAe61DtC15fgQ"
BOT_USERNAME : Final = "@chatw1thm3bot"


#Logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s}", level = logging.INFO)
logger = logging.getLogger(__name__)

#States
MOVIES_TYPE, RETURN_MENU = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start conversation and introduce book genre"""
    keyboard = [
        [InlineKeyboardButton("Thriller", callback_data="Thriller")],
        [InlineKeyboardButton("Drama", callback_data="Drama")],
        [InlineKeyboardButton("Humor", callback_data="Humor")],
        [InlineKeyboardButton("Sci-fi", callback_data="Sci-fi")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_photo(photo="images/intro2.jpg", caption="<b> Welcome Daily Movie Recommandation Bot\n" "Please choose which movie genre you want to watch</b>", parse_mode = "HTML", reply_markup=reply_markup)
    return MOVIES_TYPE

async def movie_genre(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """show movies list"""
    thrill_list = ["Gone Girl", "Seven", "Us", "Omen"]
    drama_list = ["English Patient", "Parasite", "Night"]
    humor_list = ["Girl trip", "Kit", "Up", "Town"]
    scifi_list = ["Iron man", "Dune", "Planet"]
    
    query = update.callback_query
    await query.answer()
    if query.data == "Thriller": #iterate thriller movies
        thrill_keyboard = []
        for thrill in thrill_list:
            thrill_keyboard.append([
           InlineKeyboardButton(thrill, url="t.me/thrill_movies") 
        ])
        reply_markup = InlineKeyboardMarkup(thrill_keyboard)
        await query.message.reply_text(
             f"<b> As you chose {query.data} genre. Here my today picks\n</b>",
             reply_markup = reply_markup,
             parse_mode = "HTML"
            )
    elif query.data == "Drama":
        drama_keyboard = []
        for drama in drama_list:
            drama_keyboard.append([
                InlineKeyboardButton(drama, url="t.me/drama_movies")
            ])
        reply_markup = InlineKeyboardMarkup(drama_keyboard)
        await query.message.reply_text(
            f"<b> As you chose {query.data} genre. Here my today picks❤️\n</b>",
            reply_markup = reply_markup,
            parse_mode = "HTML"
            )
    elif query.data == "Humor":
        humor_keyboard = []
        for humor in humor_list:
            humor_keyboard.append([
                InlineKeyboardButton(humor, url="t.me/drama_movies")
            ])
        reply_markup = InlineKeyboardMarkup(humor_keyboard)
        await query.message.reply_text(
            f"<b> As you chose {query.data} genre. Here my today picks❤️\n</b>",
            reply_markup = reply_markup,
            parse_mode = "HTML"
            )
    elif query.data == "Sci-fi":
        scifi_keyboard = []
        for scifi in scifi_list:
            scifi_keyboard.append([
                InlineKeyboardButton(scifi, url="t.me/drama_movies")
            ])
        reply_markup = InlineKeyboardMarkup(scifi_keyboard)
        await query.message.reply_text(
            f"<b> As you chose {query.data} genre. Here my today picks❤️\n</b>",
            reply_markup = reply_markup,
            parse_mode = "HTML"
            )



# async def return_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#      """back to start menu"""
#      await update.message.reply_markup(ReplyKeyboardMarkup("Menu"))
#      await start


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Bye Bye See you next time")
    return ConversationHandler.END

def main() -> None:
    """Run bot"""
    application = Application.builder().token(TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points= [CommandHandler("start" or "menu", start)],
        states= {MOVIES_TYPE : [MessageHandler(filters.ALL, movie_genre), CallbackQueryHandler(movie_genre)]},
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    application.add_handler(conv_handler) 
    #start  when user not in conversation
    application.add_handler(CommandHandler("start" or "menu", start))
    
    application.run_polling(poll_interval=3)
    

if __name__ == "__main__":
    main()
    
        
        