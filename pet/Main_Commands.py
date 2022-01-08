import datetime
from pet.Pet import Pet
import random
from .Tiktok_Commands import cute_message_command, play_message_command, tiktok_trend_command, clean_message_command, food_tiktok
from computer_vision.computerVision import replace_face_command
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Sticker
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
  menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
  if header_buttons:
    menu.insert(0, header_buttons)
  if footer_buttons:
    menu.append(footer_buttons)
  return menu

def action_button(update, context):
    query = update.callback_query
    group_id = update.callback_query.message.chat.id
    
    # This will define which button the user tapped on (from what you assigned to "callback_data". As I assigned them "1" and "2"):
    choice = query.data

    if choice == 'start 🐶':
        context.bot.send_message(group_id,"You can start a new pet by typing /start followed by a name. \n e.g. /start Elon Musk")
    
    if choice == 'feed 👨🏻‍🍼':
        feed_command(query, context)
    
    if choice == 'status ☁️':
        status_command(query, context)
    
    if choice == 'starve 🤤':
        starve_command(query, context)

    if choice == 'replaceFace 🐶':
        replace_face_command(query, context)
    
    if choice == 'getTiktok 🎶🐶':
        context.bot.send_message(group_id,"🐶🎶 You can use /gettiktok <hashtag> to get a random tiktok video with that hashtag. \n e.g.  /gettiktok fyp 🎶🐶")
    
    if choice == 'cuteTiktok 🥰🐶🥰':
        cute_message_command(query, context)

    if choice == 'tiktokTrend 🥳':
        tiktok_trend_command(query, context)
    
    if choice == 'cleanPet 🐶💦':
        clean_message_command(query, context)
    
    if choice == 'playPet 🐶👾':
        play_message_command(query, context)


def action_command(update, context):
    """Send a message when the command /help is issued."""    
    list_of_buttons = ["start 🐶", "feed 👨🏻‍🍼", "status ☁️", "starve 🤤", "replaceFace 🐶", 'getTiktok 🎶🐶', 'cuteTiktok 🥰🐶🥰', 'tiktokTrend 🥳', 'cleanPet 🐶💦', 'playPet 🐶👾'] 
    button_list = [] 
    for button in list_of_buttons:
        button_list.append(InlineKeyboardButton(button, callback_data=button))
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    update.message.reply_text("⚠️Here are the possible commands⚠️", reply_markup=reply_markup)


# Commands 
def start_command(update, context):
    """Send a message when the command /start is issued."""
    group_id = update["message"]["chat"]["id"]
    
    pet = Pet.get_pet(group_id)
    pet_name = " ".join(context.args)[:20]

    if pet != None and pet.is_alive():
        update.message.reply_text("🐶 You already have a pet! 🐶 Use /actions to see a list of available actions.")
        return

    if pet != None:
        if context.args:
            update.message.reply_text("Oh no\! Your pet has passed on 🥲.... \n Your new pet\, *" + pet_name +"* will be created\. 🐉 Use /actions to see a list of available actions\.", parse_mode='MarkdownV2')
            Pet.update_pet(Pet(group_id=group_id, pet_name=pet_name))
        else:
            update.message.reply_text("Oh no\! *"+pet.pet_name+"* has passed on 🥲 Use /start \<pet\_name\> to make a new pet\. 🐉", parse_mode='MarkdownV2')
        return

    if not context.args:
        update.message.reply_text("🐶 Enter a name after /start e.g. /start Elon Musk 🐶")
        return
    else:
        Pet.insert_new_pet(Pet(group_id=group_id, pet_name=pet_name))
        update.message.reply_text("🐶Your pet\, *" + pet_name + "* has been created\.🐶 Use /actions to see a list of available actions\.", parse_mode='MarkdownV2')
        return
        
    
def feed_command(update, context):
    group_id = update["message"]["chat"]["id"]
    pet = Pet.get_pet(group_id)
    if pet == None or not pet.is_alive():
        update.message.reply_text("No pet to feed 🐶")
    else:
        status_code = pet.feed()
        if status_code == 1:
            update.message.reply_text("🐶🍽*"+pet.pet_name+"* has been fed\!🍽[🐶]("+ food_tiktok() +")" + "\n ", parse_mode='MarkdownV2')
        else:
            update.message.reply_text("*"+pet.pet_name+"* is too full\.\.\. 🤢🤮", parse_mode='MarkdownV2')

def status_command(update, context):
    group_id = update["message"]["chat"]["id"]
    pet = Pet.get_pet(group_id)
    if pet == None:
        update.message.reply_text("No pet to status")
    elif not pet.is_alive():
        update.message.reply_text(pet.get_status(), parse_mode='MarkdownV2')
    else: 
        update.message.reply_text(pet.get_status(), parse_mode='MarkdownV2')

def starve_command(update, context):
    group_id = update["message"]["chat"]["id"]
    pet = Pet.get_pet(group_id)
    if pet == None or not pet.is_alive():
        update.message.reply_text("No pet to starve! 🐶")
    else:
        if pet.fullness < 10:
            pet.kill()
            update.message.reply_text("⚠️Well done\!\! *"+pet.pet_name+"* has starved to death\!⚠️", parse_mode='MarkdownV2') 
        else: 
            context.bot.send_photo(group_id, open("pet/images/starve.jpeg", "rb"))
            update.message.reply_text("⚠️Why are you starving me, you meanie!!⚠️")
            pet.starve()

    
