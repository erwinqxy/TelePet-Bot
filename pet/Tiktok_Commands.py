from TikTokApi import TikTokApi
from oauth2client import service_account
import pyshorteners
import random
from pet.Pet import Pet

#To do, add more messages 

url_shortener = pyshorteners.Shortener()
verifyFp='verify_kwwzk727_WYNGdQbf_2Bhx_4KEf_AoXP_fSMDK1IhOXEy'

def cute_message_command(update, context):
    group_id = update["message"]["chat"]["id"]
    pet = Pet.get_pet(group_id)
    if pet == None or not pet.is_alive():
        update.message.reply_text("⚠️ No pet or pet is dead. ⚠️") 
    else: 
        messages = ["Hi cutie!! :3 Anyone wanna pet me :,)🥰", "How are you guys today!! oowoo~ Please tell me more~🥰" ,
        "What should we eat today!!🥰", "Let's meet up soon guys!!🥰"] 
        i = random.randint(0, len(messages) - 1)
        update.message.reply_text(messages[i] + "\n " + cute_tiktok())
        pet.increase_happiness(2)

def clean_message_command(update, context):
    group_id = update["message"]["chat"]["id"]
    pet = Pet.get_pet(group_id)
    if pet == None or not pet.is_alive():
        update.message.reply_text("No pet or pet is dead ") 
    else: 
        link = cute_tiktok()
        messages = ["💕🥰 Aw thanks\! I feel so clean now\!\! 🥰[💕](" + link + ")", "Ah I am feeling so refreshed\!\! 🥰[💕](" + link + ")",] 
        i = random.randint(0, len(messages) - 1)
        update.message.reply_text(messages[i], parse_mode='MarkdownV2')
        pet.increase_happiness(2)

def play_message_command(update, context):
    group_id = update["message"]["chat"]["id"]
    pet = Pet.get_pet(group_id)
    if pet == None or not pet.is_alive():
        update.message.reply_text("No pet or pet is dead ") 
    else:
        link = playful_tiktok()
        messages = ["Awesome\!\! Let\'s play 👾[🐶](" + link + ")" , "About time\! I was so bored\!\! 👾[🐶](" + link + ")","OMG I WANNA PLAY\!\!\! 👾[🐶](" + link + ")"] 
        i = random.randint(0, len(messages) - 1)
        update.message.reply_text(messages[i], parse_mode='MarkdownV2')
        pet.increase_happiness(2)

def playful_tiktok():
    try:
        api = TikTokApi.get_instance(custom_verifyFp=verifyFp, use_test_endpoints=True)
        results = 10
        hashtag = "playful"
        search_results = api.by_hashtag(count=results, hashtag=hashtag)
        random_number = random.randint(0, len(search_results)-1)     ## randomize the search result to send to user 
        return (url_shortener.tinyurl.short(search_results[random_number]['video']['playAddr']))
    except:
        return "No tiktoks found"

def cute_tiktok():
    try:
        api = TikTokApi.get_instance(custom_verifyFp=verifyFp, use_test_endpoints=True)
        results = 10
        hashtag = "cute"
        search_results = api.by_hashtag(count=results, hashtag=hashtag)
        random_number = random.randint(0, len(search_results)-1)     ## randomize the search result to send to user 
        return (url_shortener.tinyurl.short(search_results[random_number]['video']['playAddr']))
    except:
        return "No tiktoks found"

def clean_tiktok():
    try:
        api = TikTokApi.get_instance(custom_verifyFp=verifyFp, use_test_endpoints=True)
        results = 10
        hashtag = "pet"
        search_results = api.by_hashtag(count=results, hashtag=hashtag)
        random_number = random.randint(0, len(search_results)-1)     ## randomize the search result to send to user 
        return (url_shortener.tinyurl.short(search_results[random_number]['video']['playAddr']))
    except:
        return "No tiktoks found"

#by hashtag
def tiktok_command(update, context):
    try:
        api = TikTokApi.get_instance(custom_verifyFp=verifyFp, use_test_endpoints=True)
        results = 10
        if context.args == []:
            update.message.reply_text("INVALID! ⚠️ Please enter a hashtag. Eg /gettiktok fyp")
        hashtag = context.args[0]

        search_results = api.by_hashtag(count=results, hashtag=hashtag)
        random_number = random.randint(0, len(search_results)-1)     ## randomize the search result to send to user 
        link = url_shortener.tinyurl.short(search_results[random_number]['video']['playAddr'])
        update.message.reply_text(text="🥰Here is a tiktok for you guys\![🥰](" + link + ")", parse_mode='MarkdownV2')
        pet.increase_happiness(2)
    except:
        update.message.reply_text("I couldn't find a tiktok :(")
        pet.increase_happiness(-1)

#by_trend
def tiktok_trend_command(update, context):
    api = TikTokApi.get_instance(custom_verifyFp=verifyFp, use_test_endpoints=True)
    results = 15
    search_results = api.by_trending(count=results)
    random_number = random.randint(0, len(search_results)-1)     ## randomize the search result to send to user 
    update.message.reply_text(url_shortener.tinyurl.short(search_results[random_number]['video']['playAddr']))


def food_tiktok():
    try:
        api = TikTokApi.get_instance(custom_verifyFp=verifyFp, use_test_endpoints=True)
        results = 10
        hashtag = "food" #maybe gordon ramsey here
        search_results = api.by_hashtag(count=results, hashtag=hashtag)
        print(search_results)
        random_number = random.randint(0, len(search_results)-1)     ## randomize the search result to send to user 
        return (url_shortener.tinyurl.short(search_results[random_number]['video']['playAddr']))
    except:
        return "No tiktoks found"