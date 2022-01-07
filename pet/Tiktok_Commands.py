from TikTokApi import TikTokApi
import pyshorteners
import random
from pet.Pet import Pet

#To do, add more messages 

url_shortener = pyshorteners.Shortener()


def cute_message_command(update, context):
    group_id = update["message"]["chat"]["id"]
    pet = Pet.get_pet(group_id)
    if pet == None or not pet.is_alive():
        update.message.reply_text("No pet or pet is dead ") 
    else: 
        messages = ["Hi cutie!! :3 Anyone wanna pet me :,)", "How are you guys today!! oowoo~ Please tell me more~" ,
        "What should we eat today!!", "Let's met up soon guys!!"] 
        i = random.randint(0, len(messages) - 1)
        update.message.reply_text(messages[i] + "\n " + cute_tiktok())

def clean_message_command(update, context):
    group_id = update["message"]["chat"]["id"]
    pet = Pet.get_pet(group_id)
    if pet == None or not pet.is_alive():
        update.message.reply_text("No pet or pet is dead ") 
    else: 
        messages = ["Aw thanks! I feel so clean now!!", "Ah I am feeling so refreshed!!",] 
        i = random.randint(0, len(messages) - 1)
        update.message.reply_text(messages[i] + "\n " + cute_tiktok())

def play_message_command(update, context):
    group_id = update["message"]["chat"]["id"]
    pet = Pet.get_pet(group_id)
    if pet == None or not pet.is_alive():
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
    return (url_shortener.tinyurl.short(search_results[random_number]['video']['playAddr']))


def cute_tiktok():
    verifyFp='verify_kwwzk727_WYNGdQbf_2Bhx_4KEf_AoXP_fSMDK1IhOXEy'
    api = TikTokApi.get_instance(custom_verifyFp=verifyFp, use_test_endpoints=True)
    results = 10
    hashtag = "cute"
    search_results = api.by_hashtag(count=results, hashtag=hashtag)
    random_number = random.randint(0, results-1)     ## randomize the search result to send to user 
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
