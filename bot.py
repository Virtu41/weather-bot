import discord
import random
import requests
import json
import os
from dotenv import load_dotenv
from discord import embeds

from discord.ext import commands

load_dotenv()
intents = discord.Intents.all() # increase functionaliy from discord.py

TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')
WEATHERKEY = os.getenv('WEATHERKEY')
CHANNEL = 0 #change channel number

client = commands.Bot(command_prefix = '?',case_insensitive=True,intents=intents) # command starts with '?'
channel = client.get_channel(CHANNEL) # specify which channel to use for some outputs

url = "https://weatherapi-com.p.rapidapi.com/current.json"

@client.event
async def on_ready(): # Start up
    print('Discord.py is working fine')
    print(f'{client.user.name} has connected to Discord!')
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    ) 

@client.command(name = 'Weather',help='Tells weather of inputted location/coordinates') # weather bot
async def weather(ctx,message):

    weather_url = f"https://weatherapi-com.p.rapidapi.com/current.json"

    querystring = {"q":message}

    headers = {
	    "X-RapidAPI-Key": WEATHERKEY,
	    "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }

    response = requests.get(weather_url, headers=headers, params=querystring)
    print(response.json())
    data = response.json()
    location = data['location']
    current = data['current']
    name = location['name'].capitalize()
    region = location['region'].capitalize()
    country = location['country'].capitalize()
    tempc = current['temp_c']
    date = current['last_updated']
    image = current['condition']['icon']
    weather = current['condition']['text']
    feelc = current['feelslike_c']
    windkph = current['wind_kph']
    winddir = current['wind_dir']
    humidity = current['humidity']
    result = discord.Embed(title = f"{name}, {region}, {country}") # location
    result.add_field(name = "Weather:", value = f"{weather}", inline=False) # weather
    result.add_field(name = "Temperature:", value = f"{tempc}{chr(176)}C", inline=False) # temperature
    result.add_field(name = "Feels like:", value = f"{feelc}{chr(176)}C", inline=False) # feels like temperature
    result.add_field(name = "Humidity:", value = f"{humidity}%", inline=False) # humidity
    result.add_field(name = "Wind speed:", value = f"{windkph} km/h", inline=False) # wind speed
    result.add_field(name = "Wind direction:", value = f"{winddir}", inline=False) # wind direction
    result.add_field(name = "Time reported:", value = date, inline = False) # time reported
    result.set_image(url = f"https:{image}") 

    await ctx.send(embed=result)
    

client.run (TOKEN)
