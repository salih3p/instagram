from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

# Bot token and admin ID
BOT_TOKEN = "6849425629:AAEky0ZyqtAzifO_1cKqXPFSzlNkaE9U_TU"
ADMIN_CHAT_ID = 6389146980

# Authentication list (replace with valid user IDs)
valid_users = ['6389146980']  # Replace with actual authenticated user ID

def start(update: Update, context: CallbackContext):
    if str(update.effective_chat.id) in valid_users:
        update.message.reply_text("Welcome! Please send the Instagram ID you want to report.")
    else:
        update.message.reply_text("You are not authorized to use this bot.")

def handle_instagram_id(update: Update, context: CallbackContext):
    if str(update.effective_chat.id) in valid_users:
        instagram_id = update.message.text
        context.user_data['instagram_id'] = instagram_id

        # Show an inline button for confirmation
        keyboard = [
            [InlineKeyboardButton("Confirm and Send", callback_data='confirm_send')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(f"Instagram ID: {instagram_id}. Click the button below to send this to the admin.", reply_markup=reply_markup)
    else:
        update.message.reply_text("You are not authorized to use this bot.")

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == 'confirm_send':
        instagram_id = context.user_data.get('instagram_id')
        
        # Get the username or user ID of the person who sent the message
        user = query.from_user
        username = user.username if user.username else f"ID: {user.id}"
        
        # Send the message to the admin
        if instagram_id:
            admin_message = f"Instagram Ban Request\nSender: @{username}\nTarget Instagram ID: {instagram_id}"
            context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_message)

            query.message.reply_text("Instagram ID has been sent to the admin.")
        else:
            query.message.reply_text("Error: No Instagram ID found.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_instagram_id))
    dp.add_handler(CallbackQueryHandler(button_handler))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
