import datetime
from pet.Pet import Pet
import random
from .Tiktok_Commands import food_tiktok
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Sticker
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler


food_dict = {'MILK TEA WITH PEARLS': 2, 'MCSPICY UPSIZED': 3, 'PET FOOD': 4, 'MALA XIANGUO': 5}   #todo: fix the food items 


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

    if choice == 'actions 🐶':
        context.bot.send_message(group_id,"🐶 - You can view the possible actions using /actions")

    if choice == 'kill 💀':
        context.bot.send_message(group_id,"💀 - You can kill your pet by typing /kill HEHEHE")
    
    if choice == 'feed 👨🏻‍🍼':
        context.bot.send_message(group_id,"👨🏻‍🍼 - You can feed your pet by typing /feed followed by a food name. \n Use /getFood to see the list of food items.")
    
    if choice == 'getFood 🍽':
        context.bot.send_message(group_id,"🍽🌭 You can use /getFood to get a list of food items that your pet loves. 🍔🍽)")
    
    if choice == 'status ☁️':
        context.bot.send_message(group_id,"☁️ You can use /status to get the status of your pet ❤️ ☁️ ")
    
    if choice == 'age 🐶':
        context.bot.send_message(group_id,"🐶 You can use /age to get the age of your pet 🐶")
    
    if choice == 'starve 🤤':
        context.bot.send_message(group_id,"🤤 You can starve your pet using /starve 🤤)")

    if choice == 'replaceFace 🐶':
        context.bot.send_message(group_id,"🐶 You can use /replaceFace to replace your pet's AI face 🐶")
    
    if choice == 'getTiktok 🎶🐶':
        context.bot.send_message(group_id,"🐶🎶 You can use /getTiktok <hashtag> to get a random tiktok video with that hashtag. \n e.g.  /getTiktok fyp 🎶🐶")
    
    if choice == 'cuteTiktok 🥰🐶🥰':
        context.bot.send_message(group_id,"🥰🐶 You can use /cuteTiktok to get a random cute tiktok video 🐶🥰")

    if choice == 'tiktokTrend 🥳':
        context.bot.send_message(group_id,"🥳 You can use /tiktokTrend to get a random trending tiktok video 🥳")
    
    if choice == 'cleanPet 🐶💦':
        context.bot.send_message(group_id,"💦🐶 You can use /cleanPet to clean your pet hehe! 🐶💦")
    
    if choice == 'playPet 🐶👾':
        context.bot.send_message(group_id,"🐶👾 You can use /playPet to play with your pet 👾🐶")


def action_command(update, context):
    """Send a message when the command /help is issued."""    
    list_of_buttons = ["start 🐶", "actions 🐶", "kill 💀", "feed 👨🏻‍🍼", "getFood 🍽", "status ☁️", "age 🐶", "starve 🤤", "replaceFace 🐶", 'getTiktok 🎶🐶', 'cuteTiktok 🥰🐶🥰', 'tiktokTrend 🥳', 'cleanPet 🐶💦', 'playPet 🐶👾'] 
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
    pet_name = " ".join(context.args)

    if pet != None and pet.is_alive():
        update.message.reply_text("🐶 You already have a pet! 🐶")
        return

    if pet != None:
        if context.args:
            update.message.reply_text("Oh no! Your pet has passed on 🥲.... \n Your new pet, " + pet_name +" will be created. 🐉")
            Pet.update_pet(Pet(group_id=group_id, pet_name=pet_name))
        else:
            update.message.reply_text("Oh no! Your pet has passed on 🥲 Use /start <pet_name> to make a new pet. 🐉")
        return

    if not context.args:
        update.message.reply_text("🐶 Enter a name after /start e.g. /start Elon Musk 🐶")
        return
    else:
        Pet.insert_new_pet(Pet(group_id=group_id, pet_name=pet_name))
        update.message.reply_text("🐶 ||Your pet, " + pet_name + " has been created. ||🐶", parse_mode='MarkdownV2')
        return
        
def kill_command(update, context):
    group_id = update["message"]["chat"]["id"]
    pet = Pet.get_pet(group_id)
    if pet == None or not pet.is_alive():
        update.message.reply_text("No pet to kill!! 🐶")
    else: 
        context.bot.send_photo(group_id, open("pet/images/death.jpeg", "rb"))
        update.message.reply_text("Your pet has been killed! 🐶")
        pet.kill()

    
def feed_command(update, context):
    group_id = update["message"]["chat"]["id"]
    pet = Pet.get_pet(group_id)
    if pet == None or not pet.is_alive():
        update.message.reply_text("No pet to feed 🐶")
    elif not context.args: 
        update.message.reply_text("Please choose a food using /getfood 🍽")
    else:
        food = " ".join(context.args)

        status_code = pet.feed(food)

        if status_code == 2:
            update.message.reply_text("🤢🤮 Yucks I dont like that food. 🤢🤮")
        elif status_code == 1:
            update.message.reply_text("🐶🍽Your pet has been fed!🍽🐶")
        else:
            update.message.reply_text("Problem feeding your pet... 🤢🤮")


def status_command(update, context):
    group_id = update["message"]["chat"]["id"]
    pet = Pet.get_pet(group_id)
    print(pet.pet_name)
    if pet == None:
        update.message.reply_text("No pet to status")
    elif not pet.is_alive():
        update.message.reply_text(pet.get_status())
    else: 
        update.message.reply_text(pet.get_status())

def age_command(update, context):
    group_id = update["message"]["chat"]["id"]
    pet = Pet.get_pet(group_id)
    if pet == None or not pet.is_alive():
        update.message.reply_text("⚠️ No pet to age! ⚠️")
    else: 
        update.message.reply_text("Your pet is " + str(pet.get_age()) + " days old. 🐶")

def starve_command(update, context):
    group_id = update["message"]["chat"]["id"]
    pet = Pet.get_pet(group_id)
    if pet == None or not pet.is_alive():
        update.message.reply_text("No pet to starve! 🐶")
    else:
        if pet.fullness < 10:
            pet.kill()
            update.message.reply_text("⚠️Well done!! Your pet has starved to death!⚠️") 
        else: 
            context.bot.send_photo(group_id, open("pet/images/starve.jpeg", "rb"))
            update.message.reply_text("⚠️Why are you starving me, you meanie!!⚠️")
            pet.starve()

def get_food_command(update, context):
    group_id = update["message"]["chat"]["id"]
    pet = Pet.get_pet(group_id)
    if pet == None or not pet.is_alive():
        update.message.reply_text("⚠️ Your pet is not alive! ⚠️")
    else:
        message_list = "Food Available are [<food name> - <food points>]: \n"
        for i in range(len(food_dict)):
            message_list += str(i+1) + ". " + (list(food_dict.keys())[i] + " - " + str(food_dict[list(food_dict.keys())[i]]) + " food points\n")
        update.message.reply_text(message_list)



'''
def face_command(update, context):
    group_id = update["message"]["chat"]["id"]
    print(update)
    print('\n')
    print(context.args)
    context.bot.send_photo(group_id, open("petpet/inference-img2.jpg", "rb"))
    update.message.reply_text("processing image")


    #https://api.telegram.org/bot5007007064:AAETfWXVt6Z4ilnW7-Rlltz43NmScS1JTAc/getFile
'''
'''
def downloader(update, context):
    print(update.message)
    context.bot.get_file(update.message.document).download()
    
    with open("petpet/images/test.jpeg", 'wb') as f:
        context.bot.get_file(update.message.document).download(out=f)
'''


    
