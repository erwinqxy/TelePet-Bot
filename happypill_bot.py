#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from pet.Main_Commands import start_command, action_command, feed_command, status_command, starve_command, action_button
from pet.Tiktok_Commands import cute_message_command, clean_message_command, play_message_command, tiktok_trend_command, tiktok_command
from computer_vision.computerVision import face_handler_static,face_handler_dynamic,replace_face_command,button,send_gif_command

TOKEN = None
PORT = int(os.environ.get('PORT', 5000))

with open("token.txt") as f:
    TOKEN = f.read().strip()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def echo(update, context):
    """Echo the user message."""
    #print(update.message)
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

    # Computer Vision COmmands 
    #dp.add_handler(CommandHandler("face", face_command))
    # dp.add_handler(CommandHandler("updateOverlay", update_overlay_command))
    # dp.add_handler(MessageHandler(Filters.photo, face_handler))
    #dp.add_handler(MessageHandler(Filters.photo, update_overlay_func))

    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text, echo))

    #dp.add_handler(MessageHandler(Filters.photo, handle))

    dp.add_handler(CommandHandler("sendgif", send_gif_command))
    
    dp.add_handler(CommandHandler("replaceface", replace_face_command))
    dp.add_handler(MessageHandler(Filters.photo | Filters.sticker, face_handler_static))
    dp.add_handler(MessageHandler(Filters.document, face_handler_dynamic))
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
    #updater.start_polling()
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    updater.bot.set_webhook('https://agile-gorge-67051.herokuapp.com/'+TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()


