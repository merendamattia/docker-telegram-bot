# Telethon utility # pip install telethon
from telethon import TelegramClient, events
from telethon.tl.custom import Button

# Scripts utility
from scripts import btc_script

import configparser # Library for reading from a configuration file, # pip install configparser
import datetime # Library that we will need to get the day and time, # pip install datetime

import asyncio

#### Access credentials
config = configparser.ConfigParser() # Define the method to read the configuration file
config.read('config.ini') # read config.ini file

api_id = config.get('default','api_id') # get the api id
api_hash = config.get('default','api_hash') # get the api hash
BOT_TOKEN = config.get('default','BOT_TOKEN') # get the bot token

# Create the client and the session called session_master. We start the session as the Bot (using bot_token)
client = TelegramClient('sessions/session_master', api_id, api_hash).start(bot_token=BOT_TOKEN)


# Define the /start command
@client.on(events.NewMessage(pattern='/(?i)start'))
async def start(event):
    sender = await event.get_sender()
    SENDER = sender.id
    USERNAME = sender.username
    text = "Benvenuto nel bot dei calabresi, " + str(USERNAME) + "!"
    await client.send_message(SENDER, text, parse_mode="HTML")


# Define the /stop command
@client.on(events.NewMessage(pattern='/(?i)stop')) 
async def stop(event):
    sender = await event.get_sender()
    SENDER = sender.id
    text = "Bot is stopping. Adios!"
    await client.send_message(SENDER, text, parse_mode="HTML")

    # Stop the bot execution
    await client.disconnect()


### Test command
@client.on(events.NewMessage(pattern='/(?i)hi')) 
async def time(event):
    # Get the sender of the message
    sender = await event.get_sender()
    SENDER = sender.id
    USERNAME = sender.username
    text = "Hi " + str(USERNAME) + "!"
    await client.send_message(SENDER, text, parse_mode="HTML")


### Test command, get the current time and day
@client.on(events.NewMessage(pattern='/(?i)time')) 
async def time(event):
    # Get the sender of the message
    sender = await event.get_sender()
    SENDER = sender.id
    text = "Received! Day and time: " + str(datetime.datetime.now())
    await client.send_message(SENDER, text, parse_mode="HTML")


### BTC fees command, get current fees on Bitcoin Blockchain
@client.on(events.NewMessage(pattern='/(?i)btcfees')) 
async def time(event):
    # Get the sender of the message
    sender = await event.get_sender()
    SENDER = sender.id
    text = btc_script.btc_fees()
    await client.send_message(SENDER, text, parse_mode="HTML")


### BTC tracking fees command, get a notify when the current fee is under a target on Bitcoin Blockchain
@client.on(events.NewMessage(pattern='/(?i)trackbtcfees (.+)')) 
async def time(event):
    # Get the sender of the message
    sender = await event.get_sender()
    SENDER = sender.id
    
    user_message = event.pattern_match.group(1)  # Estrai il messaggio dall'input

    # Controllo se user_message è un numero
    if user_message.isdigit():
        # Se è un numero, fai qualcosa
        response_text = f"You entered a number: {user_message}"
        await event.respond(response_text)
        
        # btc_script.tracking_function_btcfees(user_message, event)
        loop = asyncio.get_event_loop()
        loop.create_task(btc_script.tracking_function_btcfees(user_message, event))

        response_text = f"Tracking started"
        await event.respond(response_text)
    else:
        # Se non c'è nessun messaggio
        response_text = "You didn't provide any message."

### MAIN
if __name__ == '__main__':
    print("Bot Started!")
    client.run_until_disconnected()
