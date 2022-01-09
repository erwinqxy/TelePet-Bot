#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
PORT = int(os.environ.get('PORT', 8443))

from pet.Pet import Pet
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from pet.Main_Commands import start_command, action_command, feed_command, status_command, starve_command, action_button
from pet.Tiktok_Commands import cute_message_command, clean_message_command, play_message_command, tiktok_trend_command, tiktok_command
from computer_vision.computerVision import face_handler_static,face_handler_dynamic,replace_face_command,button,send_gif_command

TOKEN = "5074305131:AAEYfqQBxhZl8Ecl5J6Bw-nv5HAtlfBQRSU"
TOKEN = "5007007064:AAETfWXVt6Z4ilnW7-Rlltz43NmScS1JTAc" # zhili

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def handle(update, context):
    file = update.message.photo[-1].file_id
    obj = context.bot.get_file(file)
    obj.download()
    update.message.reply_text("Image received")


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary

    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram

    # General Commands 
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("actions", action_command))
    dp.add_handler(CommandHandler("feed", feed_command))
    dp.add_handler(CommandHandler("status", status_command))
    dp.add_handler(CommandHandler("starve", starve_command))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))

    # Computer Vision Commands 
    dp.add_handler(CommandHandler("sendgif", send_gif_command))
    dp.add_handler(CommandHandler("replaceface", replace_face_command))
    dp.add_handler(MessageHandler(Filters.photo | Filters.sticker, face_handler_static))
    dp.add_handler(MessageHandler(Filters.document, face_handler_dynamic))
    #dp.add_handler(MessageHandler(Filters.photo, handle))
    #dp.add_handler(MessageHandler(Filters.sticker, sticker_handler))

    #Magic Code
    def douknowwhatsgoingonhere(button1, button2):
        def neverlearnyourhigherorderfunctionsproperly(update, context):
            button1(update, context)
            button2(update, context)
        return neverlearnyourhigherorderfunctionsproperly

    dp.add_handler(CallbackQueryHandler(douknowwhatsgoingonhere(button, action_button)))


    # Tiktok Commands 
    dp.add_handler(CommandHandler("gettiktok", tiktok_command))
    dp.add_handler(CommandHandler("cutetiktok", cute_message_command))
    dp.add_handler(CommandHandler("cleanPet", clean_message_command))
    dp.add_handler(CommandHandler("playPet", play_message_command))
    dp.add_handler(CommandHandler("tiktoktrend", tiktok_trend_command))


    # log all errors
    dp.add_error_handler(error)

    '''
    def docmsg(update, context):
        if update.message.document.mime_type == "video/mp4":
            print("This is a GIF!")
    
    dp.add_handler(MessageHandler(Filters.document, docmsg))
    '''
    # Start the Bot
    updater.start_polling()
    #updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    #updater.bot.set_webhook('https://agile-gorge-67051.herokuapp.com/'+TOKEN)

    '''
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url = 'https://telepet.herokuapp.com/' + TOKEN)
    '''

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()


