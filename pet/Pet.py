import datetime
from functools import update_wrapper
from re import L
import gspread
from gspread import worksheet
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('google_api_key.json',scope)
client = gspread.authorize(creds)
sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1Oy3Y4g2xPQBIfeEZEcLI8JSr2W6UTFKeLFG2SZ4M-2I/edit?usp=sharing').sheet1
#result = sheet.get_all_records()

#print(result)

# Pet Object 
class Pet:
    pet_name = "" 
    group_id = -1
    isAlive = False 
    start_date = None
    last_updated = None
    fullness = 0
    happiness = 0   # happiness level can correspond to messages receieved from the users / can be seen as points  #to do: is there a threshold / limit
    lives = 5 
    
    def __init__(self, group_id, isAlive=True, start_date=datetime.datetime.now(), last_updated=datetime.datetime.now(), fullness=100, happiness=0, lives=5, pet_name="Cinnabois"):
        self.pet_name = pet_name
        self.group_id = group_id
        self.isAlive = isAlive
        self.start_date = start_date
        self.last_updated = last_updated
        self.fullness = fullness
        self.happiness = happiness
        self.lives = lives
    
    def kill(self) -> None: 
        self.isAlive = False
        self.fullness = 0
        self.lives = 0
        Pet.update_pet(self)

    def is_alive(self) -> bool:
        return self.isAlive
    
    def feed(self) -> int:
        if round(self.fullness) < 100:
            self.fullness = min(self.fullness + 3, 100)
            Pet.update_pet(self)
            return 1
        return 0
    
    def get_status(self) -> str:
        # can add emojis to the status
        if not self.is_alive():
            return "Your pet has moved on... :( use /start to get a new pet 🐶"
        return " \n🐶 Your pet\, *" + self.pet_name +  "* is " + str(self) + " 🐶 \n🐶 *" + self.pet_name +"* is *"+ str(self.get_age())+"* days old 🐶 \n🤩 Pet fullness level is: *" + str(round(self.fullness)) + "*🤩 \n🥰 Pet happiness level is: *" + str(round(self.happiness)) + "* 🥰\n😇 Pet lives left: *" + str(self.lives) + "* 😇"

    def get_age(self) -> float:
        return (datetime.datetime.now() - self.start_date).days

    def starve(self) -> None:
        self.fullness -= 1
        if self.fullness < 50:
            self.lose_live()
        Pet.update_pet(self)

    def lose_live(self, lives) -> None:
        curr_lives = self.lives - lives
        if curr_lives <= 0:
            self.kill()
            Pet.update_pet(self)
            return "⚠️ Your pet has died! ⚠️"
        else:
            Pet.update_pet(self)
            return "⚠️ Your pet has lost a life! \n NOTICE: Your pet have " + str(curr_lives) + " lives left! ⚠️"
    
    def get_lives(self) -> int:
        return self.lives

    def update_pet_hunger(self):
        if not self.is_alive():
            return
        hunger_per_hour = 3
        happiness_per_hour = 3
        hours_elapsed = (datetime.datetime.now() - self.last_updated).seconds / 3600
        new_updated = datetime.datetime.now()
        fullness_subtracted = hunger_per_hour*hours_elapsed
        happiness_subtracted = happiness_per_hour*hours_elapsed
        intermediate_fullness = self.fullness - fullness_subtracted
        self.happiness = max(0, self.happiness - happiness_subtracted)
        if intermediate_fullness > 0:
            self.fullness = intermediate_fullness
            self.last_updated = new_updated
            return

        lives_lost = intermediate_fullness//-100 + 1
        resultant_fullness = intermediate_fullness%100
        self.lose_live(lives_lost)
        self.fullness = resultant_fullness
        return

    def increase_happiness(self, value):
        self.happiness = max(min(self.happiness + value, 100), 0)
        Pet.update_pet(self)

    def __str__(self) -> str:
        if self.isAlive: 
            return "alive"
        else:
            return "is dead"

    @staticmethod
    def insert_new_pet(pet):
        sheet.append_row([str(pet.group_id), pet.isAlive, str(pet.start_date), str(pet.last_updated), pet.fullness, pet.happiness, pet.lives, pet.pet_name], "USER_ENTERED")

    @staticmethod
    def get_pet(group_id):
        cell = sheet.find(str(group_id))
        if not cell:
            return None
        values = sheet.row_values(cell.row)

        pet = Pet(values[0], values[1] == "TRUE", datetime.datetime.strptime(values[2], "%Y-%m-%d %H:%M:%S"), datetime.datetime.strptime(values[3], "%Y-%m-%d %H:%M:%S"), float(values[4]), float(values[5]), int(values[6]), values[7])
        pet.update_pet_hunger()
        Pet.update_pet(pet)

        return pet

    @staticmethod
    def update_pet(pet):
        cell = sheet.find(str(pet.group_id))
        if not cell:
            return False
        sheet.update("B{}:H{}".format(cell.row, cell.row), [[pet.isAlive, str(pet.start_date), str(pet.last_updated), pet.fullness, pet.happiness, pet.lives, pet.pet_name]], raw=False)
        return True