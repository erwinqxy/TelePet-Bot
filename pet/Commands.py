import datetime
from pet.pet import Pet

# Store Pets 
pet_dict = {}    
food_dict = {'MILK TEA WITH PEARLS': 2, 'MCSPICY UPSIZED': 3, 'PET FOOD': 4, 'MALA XIANGUO': 5}   #todo: fix the food items 

from TikTokApi import TikTokApi
import pyshorteners
url_shortener = pyshorteners.Shortener()
import random

def cute_message_command(update, context):
    group_id = update["message"]["chat"]["id"]
    if group_id not in pet_dict or not pet_dict[group_id].is_alive():
        update.message.reply_text("No pet or pet is dead ") 
    else: 
        messages = ["Hi cutie!! :3 Anyone wanna pet me :,)", "How are you guys today!! oowoo~ Please tell me more~" ,
        "What should we eat today!!", "Let's met up soon guys!!"] 
        i = random.randint(0, len(messages) - 1)
        update.message.reply_text(messages[i] + "\n " + cute_tiktok())

def clean_message_command(update, context):
    group_id = update["message"]["chat"]["id"]
    if group_id not in pet_dict or not pet_dict[group_id].is_alive():
        update.message.reply_text("No pet or pet is dead ") 
    else: 
        messages = ["Aw thanks! I feel so clean now!!", "Ah I am feeling so refreshed!!",] 
        i = random.randint(0, len(messages) - 1)
        update.message.reply_text(messages[i] + "\n " + cute_tiktok())

def play_message_command(update, context):
    group_id = update["message"]["chat"]["id"]
    if group_id not in pet_dict or not pet_dict[group_id].is_alive():
        update.message.reply_text("No pet or pet is dead ") 
    else: 
        messages = ["Awesome!! Let's play", "About time! I was so bored!!","OMG I WANNA PLAY!!!"] 
        i = random.randint(0, len(messages) - 1)
        update.message.reply_text(messages[i] + "\n " + playful_tiktok())

def playful_tiktok():
    verifyFp='verify_kwwzk727_WYNGdQbf_2Bhx_4KEf_AoXP_fSMDK1IhOXEy'
    api = TikTokApi.get_instance(custom_verifyFp=verifyFp, use_test_endpoints=True)
    results = 10
    hashtag = "playful"
    search_results = api.by_hashtag(count=results, hashtag=hashtag)
    random_number = random.randint(0, results-1)     ## randomize the search result to send to user 
    print(search_results[random_number]['video']['playAddr'])
    return (url_shortener.tinyurl.short(search_results[random_number]['video']['playAddr']))


def cute_tiktok():
    verifyFp='verify_kwwzk727_WYNGdQbf_2Bhx_4KEf_AoXP_fSMDK1IhOXEy'
    api = TikTokApi.get_instance(custom_verifyFp=verifyFp, use_test_endpoints=True)
    results = 10
    hashtag = "cute"
    search_results = api.by_hashtag(count=results, hashtag=hashtag)
    random_number = random.randint(0, results-1)     ## randomize the search result to send to user 
    print(search_results[random_number]['video']['playAddr'])
    return (url_shortener.tinyurl.short(search_results[random_number]['video']['playAddr']))

#by hashtag
def tiktok_command(update, context):
    verifyFp='verify_kwwzk727_WYNGdQbf_2Bhx_4KEf_AoXP_fSMDK1IhOXEy'
    api = TikTokApi.get_instance(custom_verifyFp=verifyFp, use_test_endpoints=True)
    results = 10
    hashtag = context.args[0]
    search_results = api.by_hashtag(count=results, hashtag=hashtag)
    random_number = random.randint(0, results-1)     ## randomize the search result to send to user 
    link = url_shortener.tinyurl.short(search_results[random_number]['video']['playAddr'])
    print(link)
    update.message.reply_text(text="[Here is a tiktok for you\!](" + link + ")", parse_mode='MarkdownV2')

#by_trend
def tiktok_trend_command(update, context):
    verifyFp='verify_kwwzk727_WYNGdQbf_2Bhx_4KEf_AoXP_fSMDK1IhOXEy'
    api = TikTokApi.get_instance(custom_verifyFp=verifyFp, use_test_endpoints=True)
    results = 15
    search_results = api.by_trending(count=results)
    random_number = random.randint(0, results-1)     ## randomize the search result to send to user 
    update.message.reply_text(url_shortener.tinyurl.short(search_results[random_number]['video']['playAddr']))


def food_tiktok():
    verifyFp='verify_kwwzk727_WYNGdQbf_2Bhx_4KEf_AoXP_fSMDK1IhOXEy'
    api = TikTokApi.get_instance(custom_verifyFp=verifyFp, use_test_endpoints=True)
    results = 10
    hashtag = "food" #maybe gordon ramsey here
    search_results = api.by_hashtag(count=results, hashtag=hashtag)
    random_number = random.randint(0, results-1)     ## randomize the search result to send to user 
    print(search_results[random_number]['video']['playAddr'])
    return (url_shortener.tinyurl.short(search_results[random_number]['video']['playAddr']))

# Commands 
def start_command(update, context):
    """Send a message when the command /start is issued."""
    group_id = update["message"]["chat"]["id"]
    #todo add some messages 
    def attention_message(callback_context):
        if pet_dict[group_id].is_alive():
            callback_context.bot.send_message(group_id, text="HI EVERYONE!! Please give me some attention!!!")
            callback_context.bot.send_message(group_id, text=food_tiktok())
        else:
            callback_context.stop()

    def feeding_message(callback_context):
        if pet_dict[group_id].is_alive():
            callback_context.bot.send_message(group_id, text="HI EVERYONE!! I'm hungry!! Please feed me!!!")
        else:
            callback_context.stop()
        
    if group_id not in pet_dict or not pet_dict[group_id].is_alive():
        pet_dict[group_id] = Pet()
        update.message.reply_text("Hi! Your pet has been created.")
        t1 = random.randint(1, 24)
        t2 = random.randint(1, 5)
        # schedule message to send attention and feeding message
        context.job_queue.run_repeating(
        callback=attention_message, interval=60 * t1, context=context,) #change values to change the interval
        context.job_queue.run_repeating(
        callback=feeding_message, interval=60 * t2, context=context,)
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
        \n /updateOverlay \
        \n /kill    "
    update.message.reply_text(help)

def kill_command(update, context):
    group_id = update["message"]["chat"]["id"]
    if group_id not in pet_dict or not pet_dict[group_id].is_alive():
        update.message.reply_text("No pet to kill ")
    else: 
        context.bot.send_photo(group_id, open("petpet/images/death.jpeg", "rb"))
        update.message.reply_text("Your pet has been killed!")
        pet_dict[group_id].kill()
    

    
def feed_command(update, context):
    group_id = update["message"]["chat"]["id"]
    if group_id not in pet_dict or not pet_dict[group_id].is_alive():
        update.message.reply_text("No pet to feed ")
    elif not context.args: 
        update.message.reply_text("Please choose a food")
    else:
        food = context.args[0]
        if food not in food_dict:
            update.message.reply_text("Yucks I dont like that food.")
        else:
            update.message.reply_text("Your pet has been fed!")
            pet_dict[group_id].feed(food)

def status_command(update, context):
    group_id = update["message"]["chat"]["id"]
    if group_id not in pet_dict or not pet_dict[group_id].is_alive():
        update.message.reply_text("No pet to status ")
    else: 
        update.message.reply_text(pet_dict[group_id].get_status())

def age_command(update, context):
    group_id = update["message"]["chat"]["id"]
    if group_id not in pet_dict or not pet_dict[group_id].is_alive():
        update.message.reply_text("No pet to age!")
    else: 
        update.message.reply_text("Your pet is " + str(pet_dict[group_id].get_age()) + " days old.")

def starve_command(update, context):
    group_id = update["message"]["chat"]["id"]
    if group_id not in pet_dict or not pet_dict[group_id].is_alive():
        update.message.reply_text("No pet to starve!")
    else:
        if pet_dict[group_id].hunger >= 10:
            pet_dict[group_id].kill()
            update.message.reply_text("Well done!! Your pet has starved to death!") 
        else: 
            context.bot.send_photo(group_id, open("petpet/images/starve.jpeg", "rb"))
            update.message.reply_text("Why are you starving me, you cunt!!")
            pet_dict[group_id].starve()

def get_food_command(update, context):
    group_id = update["message"]["chat"]["id"]
    if group_id not in pet_dict or not pet_dict[group_id].is_alive():
        update.message.reply_text("Your pet is not alive!")
    else:
        message_list = "Food Available are [<food name> - <food points>]: \n"
        for i in range(len(food_dict)):
            message_list += str(i+1) + ". " + (list(food_dict.keys())[i] + " - " + str(food_dict[list(food_dict.keys())[i]]) + " food points\n")
        update.message.reply_text(message_list)

def jf_command(update, context):
    group_id = update["message"]["chat"]["id"]
    if group_id not in pet_dict or not pet_dict[group_id].is_alive():
        update.message.reply_text("No jf!")
    else:
        context.bot.send_photo(group_id, open("petpet/images/jf.jpeg", "rb"))
        update.message.reply_text("jf is here")



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


    
