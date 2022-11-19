import cloudscraper as cs
import bloxflip as bf
import bloxflip
import discord
import random
import time
from pymongo import MongoClient
from time import sleep
from bloxflip import Currency, Crash, Mines, Authorization
from discord import app_commands 

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False 

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: 
            await tree.sync() 
            self.synced = True
        print(f"We have logged in as {self.user}.")

client = aclient()
tree = app_commands.CommandTree(client)
scraper = cs.create_scraper()
mongo_url = '' #connection string
cluster = MongoClient(mongo_url)
db = cluster[''] #collection name
collection = db[''] #database name

@tree.command(name = 'login', description='login to your account') #simple login command to get user id and set balance
async def login(interaction: discord.Interaction, auth_token : str):
    user = interaction.user.id
    valid = False
    user_info = collection.find({"user": user})
    for user_info in user_info:
        valid = True
    if valid == True:
        em = discord.Embed(description=f"**<@{user}>**You are already logged in.", color=0x0025ff)
        await interaction.response.send_message(embed=em)
        return 0
    else:
        post = {'user': user, 'auth': auth_token}
        collection.insert_one(post)
        em = discord.Embed(description=f"**<@{user}> **Logged in!", color=0x0025ff)
        await interaction.response.send_message(embed=em)
        
@tree.command(name = 'real_mines', description='mines predictor') #guild specific slash command
async def self(interaction: discord.Interaction):
    user = interaction.user.id
    valid = False
    user_info = collection.find({"user": user})
    for user_info in user_info:
        valid = True
    if valid == True:
        auth_token = user_info['auth']
        
    start_time = time.time()

    r = scraper.get('https://api.bloxflip.com/games/mines/history', headers={"x-auth-token": auth_token}, params={ 'size': '1','page': '0',}  ) #send a get requests to the api to get info
    
    uuid = (r.json()['data'][0]['uuid']) #get jus the uuid (round_id) from the page

    mines_location = (r.json()['data'][0]['mineLocations']) #most recent mines location, we will use this to make a guess or a "prediction"

    clicked_spots = (r.json()['data'][0]['uncoveredLocations']) #most recent spots you clicked in yourt last game

    grid = ['❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌'] #make a 5x5 (25 total) grid

    for x in mines_location: #make each bomb postion show up on grid
        grid[x] = 'X' #change the bomb posititons to differnt character

    for x in clicked_spots: #loop through every time u clicked and make it convert to grid
        grid[x] = 'O' #change the clicked positions to differnt character
             
            
    grid =  ['❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌'] #redefine grid so it resets
                         
    roundId = int(''.join(filter(str.isdigit, uuid))) #get only numbers from round id, u could also use this to make a round id verifier

    roundNum = int(str(roundId)[:2]) #get the first two numbers out of the round id
    grid[int(roundNum / 4)] = '✔️' #change it to O to know where to click
    grid[int(roundNum / 5)] = '✔️' #change it to O to know where to click
    grid[int(roundNum / 7)] = '✔️' #change it to O to know where to click

    em = discord.Embed(color=0x0025ff)
    em.add_field(name='Grid', value="\n" + "```"+grid[0]+grid[1]+grid[2]+grid[3]+grid[4]+"\n"+grid[5]+grid[6]+grid[7]+grid[8]+grid[9]+"\n"+grid[10]+grid[11]+grid[12]+grid[13]+grid[14]+"\n"+grid[15]+grid[16]+grid[17]
    +"\n"+grid[18]+grid[19]+"\n"+grid[20]+grid[21]+grid[22]+grid[23]+grid[24] + "```\n**Response Time:**\n```" {str(int(time.time() - int(start_time)))})
    em.set_footer(text='MADE BY Geek#2526, AND MODIFIED BY static#4444')
    await interaction.response.send_message(embed=em)
    
 client.run('BOT TOKEN GOES HERE')
