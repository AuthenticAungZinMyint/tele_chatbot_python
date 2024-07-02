""""Not finished yet/ Still fixing """

from typing import Final
from telegram import Update
from telegram.ext import ( Application,
                           CommandHandler,
                           MessageHandler,
                           filters,
                           ContextTypes
                          )

#Token and bot username

TOKEN : Final = "7455922128:AAF0FhMII61CYs2sttdY5hjAe61DtC15fgQ"
BOT_USERNAME : Final = "@chatw1thm3bot"



async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """'start command to introduce chatbot"""
    await update.message.reply_text('မင်္ဂလာပါ၊ ဘာများကူညီပေးရမလဲ')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command to explain chatbot features"""
    await update.message.reply_text("ကျေးဇူးပြု၍ စာကို ရှင်းလင်းစွာ ဖော်ပြပေးပါ၊ လိုချင်သော ပစ္စည်းအမျိုးအမည်နှင့် ပေးချေလိုသော bank အမျိုးအစားအား သေချာစွာ ရွေးချယ်ပေးပါ")   

def handle_responses(text: str) -> str:
    """To auto respone what user wroted"""
    text = text.lower()
    
    book_items = {"တရားထိုင်နည်း" : 4000, "ဉာဏ်ပညာ": 3500, "ချမ်းသာနည်း" : 5000, "ငွေရှာနည်းစိတ်ပညာ" : 6000}
    
    #book_items = {}
    #book_prices = []
    #book_titles = []
     
    if "စာအုပ်" in text:
        
        #for book_item in book_items.keys():
        #    book_items.append(book_item)
        return f"{book_items.keys()}\nအထက်ပါ စာအုပ်များ instock ရှိသေးသည်။"
    elif "ဈေး" or "စျေးနှုန်း" or "စျေး" in text:
       
        #for title, price in book_items.items():
        #    book_titles.append(title)
        #    book_prices.append(price)
        return f"{book_items.keys()} : {book_items.values()} တို့ဖြစ်ပါသည်။ မည်သည့် banking ဖြင့် ငွေချေပါမည်နည်း။ wave or kpay?"
    elif "wave" or "kpay" in text:
        #if "wave":
        return "Wave - 09******* ပါ။ ဝယ်ယူမှုအတွက် ကျေးဇူးတင်ပါသည်။"
        #else:
            #return "kpay - 09******** ပါ။ ဝယ်ယူမှုအတွက် ကျေးဇူးတင်ပါသည်။"        
    else:
        return "I do not understand what you wrote."  
    
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type =  update.message.chat.type
    text = str =  update.message.text
    
    print(f"User ({update.message.chat.id}) in {message_type}: '{text}'")
    
    if message_type == "group":
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, '').strip()
            response = handle_responses(new_text)
        else:
            return
    else:
        response = handle_responses(text)
    print('Bot:', response)
    await update.message.reply_text(response)
    
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

if __name__ == "__main__":
    print("Starting...")
    app = Application.builder().token(TOKEN).build()
    
    #Add command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    
    #Message handler for all text messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    #Errors
    app.add_error_handler(error)
    #Polls
    print('Pollings....')
    app.run_polling(poll_interval=5)
    