import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('pettelebot-337219-d75bbc51adf4.json',scope)
client = gspread.authorize(creds)
sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1cK60TQMfRi9ySPWTcsBmjxbktmFzdj64pKGPmTdhGgc/edit#gid=0').sheet1
result = sheet.get_all_records()

print(result)

food_dict = {'MILK TEA WITH PEARLS': 2, 'MCSPICY UPSIZED': 3, 'PET FOOD': 4, 'MALA XIANGUO': 5}   #todo: fix the food items 


# Pet Object 
class Pet: 
    isAlive = False 
    start_date = 0
    hunger = 0
    happiness = 0   # happiness level can correspond to messages receieved from the users / can be seen as points  #to do: is there a threshold / limit
    lives = 5 

    def __init__(self) -> None:
        self.isAlive = True
        self.start_day = datetime.datetime.now()  #keep track of when the bot was created 
    
    def kill(self) -> None: 
        self.isAlive = False
    
    def is_alive(self) -> bool:
        return self.isAlive
    
    def feed(self, food) -> None:
        if self.hunger < 0:
            self.hunger -= food_dict[food]
    
    def get_status(self) -> str:
        # can add emojis to the status
        return "PET STATUS!! \n Your pet is " + str(self) + " \n Pet hunger level is: " + str(self.hunger) + " \n Pet happiness level is: " + str(self.happiness) + " \n Pet lives left: " + str(self.lives)

    def get_age(self) -> float:
        return (datetime.datetime.now() - self.start_day).days 

    def starve(self) -> None:
        self.hunger += 1
        if self.hunger > 50:
            self.lose_live() 

    def lose_live(self) -> None:
        curr_lives = self.lives - 1
        if curr_lives == 0:
            self.kill()
            return "Your pet has died!"
        else:
            self.hunger = 0
            return "Your pet has lost a life and hunger is reset! \n NOTICE: Your pet have " + str(curr_lives) + " lives left!"
    
    def get_lives(self) -> int:
        return self.lives

    def __str__(self) -> str:
        if self.isAlive: 
            return "alive"
        else:
            return "is dead"
