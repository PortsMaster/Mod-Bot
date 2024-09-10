# This example requires the 'message_content' intent.

import discord
from dotenv import load_dotenv
import os
import re

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

ignore_roles = True


ignored_roles = ["The Crew", "Port Engineers","Administrator","Port Cadets","Developer","Moderator"]

if not ignore_roles:
    ignored_roles = []

common_keywords = ["port","ported","porting","want","coming","available","about","regarding","portmaster","game","uses","made","written","programmed"]

listening_channels = ["bot-submersible","💡｜suggestion-talk"]

generic_reponse = "This is an automated response. Please check the [new-suggestion](https://discord.com/channels/1122861252088172575/1232622554984878120) channel for more information on porting."

slash_commands = {
    "/portchart": {
        "response": "Here is the portability chart https://raw.githubusercontent.com/PortsMaster/Port-Bot/main/Portmaster_chart.webp"
    },
    "!log": {
        "response": "Every port has a log.txt generated in `ports/{portfolder}`, please drag and drop it to discord for help."
    }

}

response_mappings = [
    {
        "name": "PokeMMO",
        "type": "text",
        "keywords": ["pokemmo","pokemon mmo"],
        "response": "PokeMMO can't be ported at this time."
    },
     {
        "name": "Unity",
        "type": "text",
        "keywords": ["unity"],
        "response": "Games using Unity can't be ported at this time."
    },
    {
        "name": "San Andreas",
        "type": "text",
        "keywords": ["andreas","san andreas"],
        "response": "Grand Theft Auto: San Andreas can't be ported at this time."
    }
]

load_dotenv()

def check_command(message):
    message = message.lower()
    for command in slash_commands:
        if command in message:
            return(slash_commands[command]["response"])

def parseMessage(message):
    message = message.lower()
    is_common = False
    for common in common_keywords:
        if common in message:
            is_common = True
            break
    if is_common:
        for mapping in response_mappings:
            for keyword in mapping["keywords"]:
                x = re.compile(r'\b%s\b' % keyword, re.I)
                if x.search(message):
                    response = mapping["response"] + "\n\n" + generic_reponse
                    return(response)
                
    return(False)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return
    
    response = check_command(message.content)
    if response:
        await message.reply(response)
    
    if hasattr(message.author,"roles"):
        for role in message.author.roles:
            if role.name in ignored_roles:
                return
        
    #if str(message.channel) in listening_channels:
    response = parseMessage(message.content)
    if response:
        await message.reply(response)

client.run(os.getenv('BOT_TOKEN'))
