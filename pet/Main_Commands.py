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

    if choice == 'start πΆ':
        context.bot.send_message(group_id,"You can start a new pet by typing /start followed by a name. \n e.g. /start Elon Musk")
    
    if choice == 'feed π¨π»βπΌ':
        feed_command(query, context)
    
    if choice == 'status βοΈ':
        status_command(query, context)
    
    if choice == 'starve π€€':
        starve_command(query, context)

    if choice == 'replaceFace πΆ':
        replace_face_command(query, context)
    
    if choice == 'getTiktok πΆπΆ':
        context.bot.send_message(group_id,"πΆπΆ You can use /gettiktok <hashtag> to get a random tiktok video with that hashtag. \n e.g.  /gettiktok fyp πΆπΆ")
    
    if choice == 'cuteTiktok π₯°πΆπ₯°':
        cute_message_command(query, context)

    if choice == 'tiktokTrend π₯³':
        tiktok_trend_command(query, context)
    
    if choice == 'cleanPet πΆπ¦':
        clean_message_command(query, context)
    
    if choice == 'playPet πΆπΎ':
        play_message_command(query, context)


def action_command(update, context):
    """Send a message when the command /help is issued."""    
    list_of_buttons = ["start πΆ", "feed π¨π»βπΌ", "status βοΈ", "starve π€€", "replaceFace πΆ", 'getTiktok πΆπΆ', 'cuteTiktok π₯°πΆπ₯°', 'tiktokTrend π₯³', 'cleanPet πΆπ¦', 'playPet πΆπΎ'] 
    button_list = [] 
    for button in list_of_buttons:
        button_list.append(InlineKeyboardButton(button, callback_data=button))
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    update.message.reply_text("β οΈHere are the possible commandsβ οΈ", reply_markup=reply_markup)


# Commands 
def start_command(update, context):
    """Send a message when the command /start is issued."""
    group_id = update["message"]["chat"]["id"]

    if update.message.chat.type == "private":
        update.message.reply_text("This bot can only be used in a group.")
        return

    pet = Pet.get_pet(group_id)
    pet_name = " ".join(context.args)
    pet_name = "".join(u for u in pet_name if u not in ('_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!'))
    pet_name = pet_name
    if pet != None and pet.is_alive():
        update.message.reply_text("πΆ You already have a pet! πΆ Use /actions to see a list of available actions.")
        return

    if pet != None:
        if context.args:
            update.message.reply_text("Oh no\! Your pet has passed on π₯²\.\.\.\. \n Your new pet\, *" + pet_name +"* will be created\. π Use /actions to see a list of available actions\.", parse_mode='MarkdownV2')
            Pet.update_pet(Pet(group_id=group_id, pet_name=pet_name))
        else:
            update.message.reply_text("Oh no\! *"+pet.pet_name+"* has passed on π₯² Use /start \<pet\_name\> to make a new pet\. π", parse_mode='MarkdownV2')
        return

    if not context.args:
        update.message.reply_text("πΆ Enter a name after /start e.g. /start Elon Musk πΆ")
        return
    else:
        Pet.insert_new_pet(Pet(group_id=group_id, pet_name=pet_name))
        update.message.reply_text("πΆYour pet\, *" + pet_name + "* has been created\.πΆ Use /actions to see a list of available actions\.", parse_mode='MarkdownV2')
        return
        
    
def feed_command(update, context):
    group_id = update["message"]["chat"]["id"]
    pet = Pet.get_pet(group_id)
    if pet == None or not pet.is_alive():
        update.message.reply_text("No pet to feed. Use /start <name> to create a pet. πΆ")
        return 
    else:
        status_code = pet.feed()
        if status_code == 1:
            update.message.reply_text("πΆπ½*"+pet.pet_name+"* has been fed\!π½[πΆ]("+ food_tiktok() +")" + "\n ", parse_mode='MarkdownV2')
            pet.increase_happiness(2)
            return 
        else:
            update.message.reply_text("*"+pet.pet_name+"* is too full\.\.\. π€’π€?", parse_mode='MarkdownV2')
            pet.increase_happiness(-1)
            return 

def status_command(update, context):
    group_id = update["message"]["chat"]["id"]
    pet = Pet.get_pet(group_id)
    if pet == None:
        update.message.reply_text("No pet to get status. Use /start <name> to create a pet. πΆ")
        return 
    elif not pet.is_alive():
        update.message.reply_text(pet.get_status(), parse_mode='MarkdownV2')
        return 
    else: 
        update.message.reply_text(pet.get_status(), parse_mode='MarkdownV2')
        return 

def starve_command(update, context):
    group_id = update["message"]["chat"]["id"]
    pet = Pet.get_pet(group_id)
    if pet == None or not pet.is_alive():
        update.message.reply_text("No pet to starve! Use /start <name> to create a pet. πΆ")
        return 

    else:
        if pet.fullness < 10:
            pet.kill()
            update.message.reply_text("β οΈWell done\!\! *"+pet.pet_name+"* has starved to death\!β οΈ", parse_mode='MarkdownV2') 
            return 
        else: 
            context.bot.send_photo(group_id, open("pet/images/starve.jpeg", "rb"))
            update.message.reply_text("β οΈWhy are you starving me, you meanie!!β οΈ")
            pet.starve()
            pet.increase_happiness(-2)
            return 

    
