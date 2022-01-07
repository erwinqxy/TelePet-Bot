#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

erwin_token = "5009567247:AAFMCTo_hVAp9EPcKTie-GH5o9XEgTvX6yU"
zhili_token = "5007007064:AAETfWXVt6Z4ilnW7-Rlltz43NmScS1JTAc"
jinfeng_token = "982222388:AAHSICXXWr9GhykVYyqlB6j3wWAyz0OzBzc"

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from pet.Commands import start_command, help_command, kill_command, feed_command, status_command, age_command, starve_command, jf_command \
    , get_food_command, tiktok_command, cute_message_command, clean_message_command, play_message_command, tiktok_trend_command
from computer_vision.computerVision import face_handler,replace_face_command,button

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

    erwin_token = "5009567247:AAFMCTo_hVAp9EPcKTie-GH5o9XEgTvX6yU"
    zhili_token = "5007007064:AAETfWXVt6Z4ilnW7-Rlltz43NmScS1JTAc"
    jinfeng_token = "982222388:AAHSICXXWr9GhykVYyqlB6j3wWAyz0OzBzc"

    #updater = Updater(erwin_token, use_context=True)
    updater = Updater(zhili_token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("kill", kill_command))
    dp.add_handler(CommandHandler("feed", feed_command))
    dp.add_handler(CommandHandler("status", status_command))
    dp.add_handler(CommandHandler("age", age_command))
    dp.add_handler(CommandHandler("starve", starve_command))
    dp.add_handler(CommandHandler("jf", jf_command))
    #dp.add_handler(CommandHandler("face", face_command))
    # dp.add_handler(CommandHandler("updateOverlay", update_overlay_command))
    dp.add_handler(CommandHandler("getFood", get_food_command))
    dp.add_handler(CommandHandler("tiktok", tiktok_command))
    dp.add_handler(CommandHandler("cute", cute_message_command))
    dp.add_handler(CommandHandler("clean", clean_message_command))
    dp.add_handler(CommandHandler("play", play_message_command))
    dp.add_handler(CommandHandler("tiktokTrend", tiktok_trend_command))

    # dp.add_handler(MessageHandler(Filters.photo, face_handler))
    #dp.add_handler(MessageHandler(Filters.photo, update_overlay_func))

    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text, echo))

    #dp.add_handler(MessageHandler(Filters.photo, handle))

    dp.add_handler(CommandHandler("replaceface", replace_face_command))
    dp.add_handler(MessageHandler(Filters.photo | Filters.sticker, face_handler))
    #dp.add_handler(MessageHandler(Filters.sticker, sticker_handler))
    dp.add_handler(CallbackQueryHandler(button))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()


