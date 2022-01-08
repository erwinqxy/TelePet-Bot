# TelePet 🤖
TelePet is a social butler that aims to prompt social interactions within a Telegram group environment to spark joy and laughter. This telegram bot was built for HacknRoll 2022 by #75K: Cinna-boys. Try the telegram bot [@TelePet_bot](https://t.me/TelePet_bot).

## Inspiration 🤔💭
The COVID19 pandemic has limited the frequency of human interactions. People seem to interact less with one another. And yet people are not talking to one another frequently enough, groups get incredibly foreign and awkward over time. Group Was you ever in a position where group chats are incredibly silent and awkward? Unsure what you are doing there? Were you ever in a telegram group chat that just got less active over time? We hope TelePet, a telegram bot for group chats can help bridge the gap within the virtual domain and bring people closer through simple prompts, memes, and laughter. 


## What it does 🦾
TelePet addresses aim to target the Most Entertaining Hack. 
1. Telegram group can become rather inactive and quiet. TelePet aims to spark social conversations. 
2. Telegram groups can become rather dull and lifeless. TelePet uses Computer Vision to manipulate photos, stickers, and gifs with "meme" overlays that we promise will make you laugh. 
3. Telegram groups can get quite boring with walls of text. TelePet uses Tiktok API to get random TikTok videos and the bot will send these videos in the group chat. Users can even request TikTok videos at their fingertips. 

## Set Up 
1. Add [@TelePet_bot](https://t.me/TelePet_bot) to your telegram group chat.
2. Promote the bot to group admin to allow it to access messages.
3. Send the command `/start@TelePet_bot` in your group chat and you are ready to go!

## Commands Available :computer:

| Command      | Description |
| ----------- | ----------- |
| `/start`      | Starts TelePet. You can start a new pet by typing `/start` followed by a name. e.g. `/start Elon Musk` |
| `/actions`   | You can view the available actions that the bot can execute using `/actions` |
| `/feed` |  You can feed your pet by typing `/feed`|
| `/status` |  You can use `/status` to get the status of your pet |
| `/starve` |  If you are feeling playful, you can starve your pet using /starve |
| `/replaceFace` | You can play with the computer vision feature of replacing faces in images, stickers and gifs. You can use default or custom images for the overlay image. The overlay images are stored in the local cache You can use /replaceface to activate/deactivate/replace the overlay image. |
| `/getTiktok` | You can use `/gettiktok <hashtag` to get a random tiktok video with that hashtag. e.g.  `/gettiktok fyp` |
| `/cuteTiktok` | You can use `/cutetiktok` to get a random cute tiktok video |
| `/tiktokTrend` | You can use `/tiktoktrend` to get a random trending tiktok video |
| `/cleanPet` | You can use `/cleanpet` to clean your pet |
| `/playPet` | You can use `/playpet` to play with your pet |


## How we built it 👷🏻
The backend is written in Python and [Telegram Bot API](https://core.telegram.org/bots/api). The computer vision feature was built using OpenCV2 Haar Cascade pretrained [haarcascade_frontalface_default.xml](https://github.com/opencv/opencv/tree/master/data/haarcascades) model weights for face detection. You can refer [here](https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html) for the OpenCV2 documentation. For APIs, we worked with [Tiktok API](https://dteather.com/TikTok-Api/docs/TikTokApi.html) to pull Tiktok videos, [gspread](https://docs.gspread.org/en/latest/) to set up a working database to store the pet information for each group chat in google sheets. 


## Challenges we ran into 😣
- As most of us are quite unfamiliar and inexperience working with Telegram Bot API, we had issues with the `bot`, `context commands`, `messageHandlers`, `callBackQueryHandler`. We created multiple test bots for testing purposes to familiarize ourselves with the API. Overall, we felt that we learned alot and were able to overcome it as a team and deliver the final product.  

- Encoder formats for opencv videowriter may generate videos that are incompatible for different Operating Systems (Windows vs Mac), resulting in gifs or video sent by the telegram bot to shown as a static thumbnail to IOS and Mac users in the telegram application interface.

- Integrating the Tiktok api to our bot commands. 

- Finding a free database to host our project was an issue as. However, we managed to find a solution - using a gsheet. As we are deploying the project on heroku, the dynamo will timeout and we did not want to store the pet data in the local cache. As such, we used this solution.

- As object detection models that utilizes state-of-the-art deep learning frameworks like tensorflow and pytorch would require large dependencies, large memory RAM usage and even result in a long inference time during deployment with a free tier hosted CPU runtime. The large ram usage may result in the hosted runtime to exceed to free tier memory quotas (Heroku 512mb for CPU memory). However, we found  an alternative solution to this which is to use classical computer vision algorithms such as the haar cascade algorithm for frontal face detection for our use case of replacing faces in media files.


## Accomplishments that we're proud of 🥰
- We are quite happy that we managed to use classical machine learning methods (haar cascade) for face detection and achieve a high accuracy for frontal faces in different forms of media (images, stickers and gifs).

- We are also quite proud of how we were able to integrate different APIs on Telegram to create a bot that we feel will help stimulate social integrations and bring laughters to members. 


## What we learned 🎓 
1. Using Git and GitHub 
    - We ran into many conflicts while trying to sync our changes together, working with unfamiliar APIs. With the power of google and determination, we managed to learn new concepts and ways of doing things through our mistakes and how it will be like working with other develoeprs. 
    - To help with the syncing our dicsussion, we discovered a VSCode Extension called VSCode Live Share were we able to code together in real time and reducing the risk of merge conflict. 
2. Working in a team 
    - To help with the syncing of our changes on GitHub, we also learnt to use VSCode Live Share to work together as well. This turned out to be surprisingly useful since we were unable to meet up in real life to work on the project together
3. APIs
    - We gained familiarity with using a variety of natural language APIs while we were sourcing for a suitable candidate for our application, and also had some fun along the way!
    - In addition, we had to work with a variety of AWS-related APIs to bring our solution together and we learnt about the risks of managing API keys securely.
4. Error Handling
    - We learnt how to handle exceptions and edge cases to ensure that the user input will not result in crashing the bot.
5. Computer Vision
    - The application of computer vision to the telegram bot was an eye opening experience for us and enabling us to learn the advantages as well as its limitations of AI applications.



## What's next for TelePet ⏭
- Storing cached overlay images in google drive database. 
- Using deep learning models for face detection could yield better accuracy as compared to traditional computer vision algorithms.
- We can perhaps curate a better tiktok gallery experience for the users. 
- More playful interactions between the bot and the users. 