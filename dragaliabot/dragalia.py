import discord
import os
import requests

from bs4 import BeautifulSoup

from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = discord.Client()


@bot.event
async def on_ready():
        guild_count = 0

        # LOOPS THROUGH ALL THE GUILD / SERVERS THAT THE BOT IS ASSOCIATED WITH.
        for guild in bot.guilds:
                print(f"- {guild.id} (name: {guild.name})")
                guild_count = guild_count + 1

        print("DragaliaBot is in " + str(guild_count) + " guilds.")

@bot.event
async def on_message(message):
        length = len(message.content)
        #if message.content == "hello":
        #        await message.channel.send("hey dirtbag")
        if message.content[0:3] == "dl!":
                input = message.content[3:length]
                if message.content[3] == ' ':
                        input = message.content[4:length]
                
                if input.strip() == "help":
                        await message.channel.send("stfu")
                elif input.strip() == " hello":
                        await message.channel.send("smh")
                elif not(' ' in input):
                        URL = "https://dragalialost.wiki/w/" + message.content[3:length]
                        page = requests.get(URL)

                        soup = BeautifulSoup(page.content, "html.parser")
                        results = soup.find(id="mw-content-text")

                        elements = results.find_all("div", class_="skill-display-content")

                        skillList = []

                        for element in elements:
                                paragraph = element.find("p")
                                skillList.append(paragraph.text)

                        for x in skillList:
                                print(x)
                                await message.channel.send(x)
                elif ' ' in input:
                        character = input
                        character.replace(' ', '_')
                        URL = "https://dragalialost.wiki/w/" + character
                        page = requests.get(URL)

                        soup = BeautifulSoup(page.content, "html.parser")
                        results = soup.find(id="mw-content-text")

                        elements = results.find_all("div", class_="skill-display-content")

                        skillList = []

                        for element in elements:
                                paragraph = element.find("p")
                                skillList.append(paragraph.text)

                        for x in skillList:
                                print(x)
                                await message.channel.send(x)
                                

bot.run(DISCORD_TOKEN)

