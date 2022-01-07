import datetime
from pet.Pet import Pet
import random
from .Tiktok_Commands import food_tiktok

food_dict = {'MILK TEA WITH PEARLS': 2, 'MCSPICY UPSIZED': 3, 'PET FOOD': 4, 'MALA XIANGUO': 5}   #todo: fix the food items 

# Commands 
def start_command(update, context):
    """Send a message when the command /start is issued."""
    group_id = update["message"]["chat"]["id"]
    #todo add some messages 
    def attention_message(callback_context):
        messages = ["HI EVERYONE!! Please give me some attention!!!", "HI EVERYONE!! I'm hungry!! Please feed me!!!", "ITS FEEDING TIME!!"] #todo can add more here
        pet = Pet.get_pet(group_id)
        if pet == None or not pet.is_alive():
            i = random.randint(0, len(messages)-1)
            callback_context.bot.send_message(group_id, text=messages[i])
            callback_context.bot.send_message(group_id, text=food_tiktok())
        else:
            callback_context.stop()
        
    pet = Pet.get_pet(group_id)
    if pet == None:
        Pet.insert_new_pet(Pet(group_id=group_id))
        update.message.reply_text("Hi! Your pet has been created.")
        t1 = random.randint(1, 24)
        # schedule message to send attention and feeding message
        context.job_queue.run_repeating(
        callback=attention_message, interval=60 * t1, context=context,) #change values to change the interval
    elif not pet.is_alive():
        update.message.reply_text("Hi. Your pet has died :(. A new pet will be created.")
        Pet.update_pet(Pet(group_id=group_id))
    else: 
        update.message.reply_text("You already have a pet!")
        

def help_command(update, context):
    """Send a message when the command /help is issued."""
    help = "Command List \
        \n /start  \
        \n /feed    \
        \n /status  \
        \n /age     \
        \n /starve  \
        \n /help    \
        \n /replaceface \
        \n /kill    "
    update.message.reply_text(help)


def kill_command(update, context):
    group_id = update["message"]["chat"]["id"]
    pet = Pet.get_pet(group_id)
    print(group_id)
    if pet == None or not pet.is_alive():
        update.message.reply_text("No pet to kill ")
    else: 
        context.bot.send_photo(group_id, open("pet/images/death.jpeg", "rb"))
        update.message.reply_text("Your pet has been killed!")
        pet.kill()

    
def feed_command(update, context):
    group_id = update["message"]["chat"]["id"]
    pet = Pet.get_pet(group_id)
    if pet == None or not pet.is_alive():
        update.message.reply_text("No pet to feed ")
    elif not context.args: 
        update.message.reply_text("Please choose a food /getfood")
    else:
        food = " ".join(context.args)

        status_code = pet.feed(food)

        if status_code == 2:
            update.message.reply_text("Yucks I dont like that food.")
        elif status_code == 1:
            update.message.reply_text("Your pet has been fed!")
        else:
            update.message.reply_text("Problem feeding your pet...")


def status_command(update, context):
    group_id = update["message"]["chat"]["id"]
    pet = Pet.get_pet(group_id)
    if pet == None:
        update.message.reply_text("No pet to status ")
    elif not pet.is_alive():
        update.message.reply_text(pet.get_status())
    else: 
        update.message.reply_text(pet.get_status())

def age_command(update, context):
    group_id = update["message"]["chat"]["id"]
    pet = Pet.get_pet(group_id)
    if pet == None or not pet.is_alive():
        update.message.reply_text("No pet to age!")
    else: 
        update.message.reply_text("Your pet is " + str(pet.get_age()) + " days old.")

def starve_command(update, context):
    group_id = update["message"]["chat"]["id"]
    pet = Pet.get_pet(group_id)
    if pet == None or not pet.is_alive():
        update.message.reply_text("No pet to starve!")
    else:
        if pet.fullness < 10:
            pet.kill()
            update.message.reply_text("Well done!! Your pet has starved to death!") 
        else: 
            context.bot.send_photo(group_id, open("pet/images/starve.jpeg", "rb"))
            update.message.reply_text("Why are you starving me, you cunt!!")
            pet.starve()

def get_food_command(update, context):
    group_id = update["message"]["chat"]["id"]
    pet = Pet.get_pet(group_id)
    if pet == None or not pet.is_alive():
        update.message.reply_text("Your pet is not alive!")
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


    
