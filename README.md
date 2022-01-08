# CinnaBoys 🤖
CinnaBoys is a social butler that aims to prompt social interactions within a Telegram group environment to spark joy and laughter. This telegram bot was built for HacknRoll 2022 by #75K: Cinna-boys. Try the telegram bot @


## Inspiration 🤔💭
The COVID19 pandemic has limited the frequency of human interactions. People seem to interact less with one another. And yet people are not talking to one another frequently enough, groups get incredibly foreign and awkward over time. Group Was you ever in a position where group chats are incredibly silent and awkward? Unsure what you are doing there? Were you ever in a telegram group chat that just got less active over time? We hope CinnaBoys, a telegram bot for group chats can help bridge the gap within the virtual domain and bring people closer through simple prompts, memes, and laughter. 


## What it does 🦾
CinnaBoys addresses aim to target the Most Entertaining Hack. 
1. Telegram group can become rather inactive and quiet. CinnaBoys aims to spark social conversations. 
2. Telegram groups can become rather dull and lifeless. CinnaBoys uses Computer Vision to manipulate photos, stickers, and gifs with "meme" overlays that we promise will make you laugh. 
3. Telegram groups can get quite boring with walls of text. CinnaBoys uses Tiktok API to get random TikTok videos and the bot will send these videos in the group chat. Users can even request TikTok videos at their fingertips. 


## Commands Available 

| Command      | What it does | How to use it |
| ----------- | ----------- | ----------- |
| `/start`      | <to be filled> | You can start a new pet by typing /start followed by a name. e.g. /start Elon Musk |
| `/actions`   | <to be filled> | You can view the available actions using /actions |
| `/kill` |  <to be filled> | You can kill your pet by typing /kill |
| `/feed` |  <to be filled> | You can feed your pet by typing /feed followed by a food name. Use /getfood to see the list of food items |
| `/status` |  <to be filled> | You can use /status to get the status of your pet |
| `/starve` |  <to be filled> | You can starve your pet using /starve |
| `/replaceFace` |  Enables users to play with the computer vision feature of replacing faces in images, stickers and gifs. Users can use default or custom images for the overlay image. | You can use /replaceface to replace your pet's AI face |
| `/getTiktok` |  <to be filled> | You can use /gettiktok <hashtag> to get a random tiktok video with that hashtag. e.g.  /gettiktok fyp |
| `/cuteTiktok` |  <to be filled> | You can use /cutetiktok to get a random cute tiktok video |
| `/tiktokTrend` |  <to be filled> | You can use /tiktoktrend to get a random trending tiktok video |
| `/cleanPet` |  <to be filled> | You can use /cleanpet to clean your pet |
| `/playPet` |  <to be filled> | You can use /playpet to play with your pet |


## How we built it
The backend is written in Python, with  <credits>


Database: We used google sheets API to store pet information for each group chat.


## Challenges we ran into
- JF decided to play dota and sleep 

- Encoder formats for opencv videowriter may not be compatible for different Operating Systems (Windows vs Mac), resulting in some generate videos 

## Accomplishments that we're proud of
We are quite happy that we managed to use classical machine learning methods (haar cascade) for face detection and achieve a high accuracy for frontal faces in different forms of media (images, stickers and gifs).



## What we learned 🎓 
1. Using Git and GitHub 
    - We ran into many conflicts while trying to sync our changes together, working with unfamiliar APIs, but with a fair bit of googling and endurance, we managed to pick up a few important pointers to take note of when working with other developers
    - To help with the syncing of our changes on GitHub, we also learnt to use VSCode Live Share to work together as well. This turned out to be surprisingly useful since we were unable to meet up in real life to work on the project together
2. Working in a team 
    - To help with the syncing of our changes on GitHub, we also learnt to use VSCode Live Share to work together as well. This turned out to be surprisingly useful since we were unable to meet up in real life to work on the project together
3. APIs
    - We gained familiarity with using a variety of natural language APIs while we were sourcing for a suitable candidate for our application, and also had some fun along the way!
    - In addition, we had to work with a variety of AWS-related APIs to bring our solution together and we learnt about the risks of managing API keys securely.
4. Error Handling 
5. 




## What's next for CinnaBoys 

More support for


